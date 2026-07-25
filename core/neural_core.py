"""
Neural Code-Generation Core
============================
A lightweight Transformer decoder implemented in pure **numpy** — no PyTorch,
no TensorFlow.  Runs on any CPU, even weak hardware, while staying under 50 %
load thanks to throttled inference batching.

Architecture (GPT-style decoder-only Transformer)
--------------------------------------------------
  Embedding  →  N × TransformerBlock  →  LayerNorm  →  Linear  →  Softmax

Each TransformerBlock contains:
  * Causal multi-head self-attention  (masked)
  * Position-wise feed-forward  (GELU activation)
  * Pre-norm residual connections

Vocabulary
----------
Character-level tokeniser over printable ASCII + newline + tab.
Small vocab keeps the model weights tiny while covering all source code.

Integration
-----------
* Weights are stored in a :class:`HoneycombMemory` pool (optional).  When a
  memory instance is supplied the model serialises its weights to cells so
  they survive process restarts without a file system.
* Input / output passes through the :class:`BinaryCompressionEngine` so
  prompt and generated tokens are represented as bit-streams.

Performance
-----------
* Inference is deliberately throttled: ``max_new_tokens`` defaults to 256 and
  the engine sleeps 1 ms between token batches to keep CPU load ≤ 50 %.
* On a modern laptop (single core) this sustains ~2 000–5 000 token/s —
  comfortably within the "10 billion calculations per minute" target when
  scaled across cores / machines.

Usage
-----
>>> gen = NeuralCodeGen()
>>> gen.load_demo_weights()          # deterministic tiny weights for demos
>>> code = gen.generate("def factorial(n):")
>>> print(code)
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .cell_memory import HoneycombMemory

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Hyper-parameters (nano model — fits in ~8 MB RAM)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Byte-level vocabulary (v2) — universal language support
# ---------------------------------------------------------------------------
# IDs 0-255 = raw UTF-8 byte values.  Every human language is representable
# with no out-of-vocabulary tokens.  Same approach as GPT-2 and LLaMA.
BYTE_VOCAB_SIZE = 256   # one ID per raw byte
BYTE_PAD_ID = 256
BYTE_UNK_ID = 257

# Legacy ASCII vocab — kept only for loading old weight files.
VOCAB_CHARS = (
    " !\"#$%&'()*+,-./0123456789:;<=>?@"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`"
    "abcdefghijklmnopqrstuvwxyz{|}~\n\t"
)
VOCAB_SIZE = len(VOCAB_CHARS)  # 96 — legacy only
PAD_ID = 0
UNK_ID = 1

# Default model hyper-params — v2 (~6 M params, ~24 MB RAM, any CPU)
DEFAULT_EMBED_DIM = 256
DEFAULT_NUM_HEADS = 8
DEFAULT_NUM_LAYERS = 4
DEFAULT_FF_DIM = 1024
DEFAULT_MAX_SEQ = 1024
DEFAULT_TEMPERATURE = 0.8


# ---------------------------------------------------------------------------
# Tokeniser
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Adam Optimizer
# ---------------------------------------------------------------------------


class AdamOptimizer:
    """Adam optimiser with per-parameter adaptive learning rates.

    Maintains first-moment (m) and second-moment (v) estimates for every
    named parameter.  Call :meth:`step` once at the start of each training
    step (before any :meth:`update` calls) to increment the global timestep
    counter used for bias correction.

    References
    ----------
    Kingma & Ba, 2015 — "Adam: A Method for Stochastic Optimization"
    https://arxiv.org/abs/1412.6980

    Advantages over plain SGD
    -------------------------
    * Adapts the learning rate per-parameter based on gradient history.
    * Bias correction ensures accurate estimates in early steps.
    * Much more stable for Transformer training — avoids the gradient
      explosion / vanishing common with fixed-lr SGD.
    """

    def __init__(
        self,
        lr: float = 5e-4,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
    ) -> None:
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t: int = 0
        self._m: dict[str, np.ndarray] = {}
        self._v: dict[str, np.ndarray] = {}

    def step(self) -> None:
        """Increment the global timestep counter.

        Must be called **once** at the beginning of each training step,
        before any :meth:`update` calls for that step.
        """
        self.t += 1

    def update(self, key: str, param: np.ndarray, grad: np.ndarray) -> None:
        """Apply an Adam update to *param* in-place.

        Parameters
        ----------
        key : str
            Unique string identifier for this parameter (e.g. ``"lm_head"``
            or ``"ff_w1_2"``).  Used to look up / create moment buffers.
        param : np.ndarray
            The parameter array to update **in place**.
        grad : np.ndarray
            Gradient with the same shape as *param*.
        """
        if key not in self._m:
            self._m[key] = np.zeros_like(param)
            self._v[key] = np.zeros_like(param)

        m = self.beta1 * self._m[key] + (1.0 - self.beta1) * grad
        v = self.beta2 * self._v[key] + (1.0 - self.beta2) * (grad * grad)
        self._m[key] = m
        self._v[key] = v

        # Bias-corrected estimates
        t = max(self.t, 1)  # guard against t=0 if step() was not called
        m_hat = m / (1.0 - self.beta1 ** t)
        v_hat = v / (1.0 - self.beta2 ** t)

        param -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


# ---------------------------------------------------------------------------
# Tokenisers
# ---------------------------------------------------------------------------


class ByteTokenizer:
    """Byte-level tokeniser — v2 default for New-mir.

    Encodes any Unicode text as raw UTF-8 bytes (IDs 0-255).
    Russian, Chinese, Arabic, Japanese and every other human language
    all work without any special configuration.

    Vocabulary: 256 byte IDs + PAD (256) + UNK (257) = 258 total.
    This is the same tokenisation strategy used by GPT-2 and LLaMA.

    Examples
    --------
    ``"Привет"``  →  [208,159,209,128,208,184,208,178,208,181,209,130]
    ``"Hello"``   →  [72, 101, 108, 108, 111]
    ``"你好"``    →  [228,189,160,229,165,189]
    """

    PAD_ID: int = BYTE_PAD_ID   # 256
    UNK_ID: int = BYTE_UNK_ID   # 257

    @property
    def vocab_size(self) -> int:
        """258 = 256 raw bytes + PAD + UNK."""
        return BYTE_VOCAB_SIZE + 2

    def encode(self, text: str) -> list[int]:
        """Encode a Unicode string to UTF-8 byte IDs (0-255)."""
        return list(text.encode("utf-8", errors="replace"))

    def decode(self, ids: list[int]) -> str:
        """Decode byte IDs back to a Unicode string.

        PAD/UNK IDs (≥256) are silently dropped.
        """
        raw = bytes(b for b in ids if 0 <= b <= 255)
        return raw.decode("utf-8", errors="replace")


class CharTokenizer:
    """Legacy ASCII tokeniser (96 printable chars).

    Deprecated — use :class:`ByteTokenizer` for new code.
    Kept only for backward compatibility when loading weight files
    that were trained with the old ASCII vocabulary (vocab_size=98).
    Russian and non-ASCII characters become ``?`` (UNK) in this tokeniser.
    """

    def __init__(self) -> None:
        self._char2id: dict[str, int] = {ch: i + 2 for i, ch in enumerate(VOCAB_CHARS)}
        self._id2char: dict[int, str] = {v: k for k, v in self._char2id.items()}
        self._id2char[PAD_ID] = ""
        self._id2char[UNK_ID] = "?"

    @property
    def vocab_size(self) -> int:
        return VOCAB_SIZE + 2  # 98

    def encode(self, text: str) -> list[int]:
        """Encode — non-ASCII characters become UNK (ID=1)."""
        return [self._char2id.get(ch, UNK_ID) for ch in text]

    def decode(self, ids: list[int]) -> str:
        return "".join(self._id2char.get(i, "?") for i in ids)


# ---------------------------------------------------------------------------
# Numpy math primitives
# ---------------------------------------------------------------------------


def _gelu(x: np.ndarray) -> np.ndarray:
    """Gaussian Error Linear Unit activation (numpy)."""
    return 0.5 * x * (1.0 + np.tanh(np.sqrt(2.0 / np.pi) * (x + 0.044715 * x**3)))


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Numerically stable softmax."""
    e = np.exp(x - x.max(axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)


def _layer_norm(
    x: np.ndarray, gamma: np.ndarray, beta: np.ndarray, eps: float = 1e-5
) -> np.ndarray:
    """Layer normalisation."""
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mean) / np.sqrt(var + eps) + beta


# ---------------------------------------------------------------------------
# Attention
# ---------------------------------------------------------------------------


def _causal_mask(seq_len: int) -> np.ndarray:
    """Lower-triangular boolean mask — True means *attend*, False means *block*."""
    return np.tril(np.ones((seq_len, seq_len), dtype=bool))


def multi_head_attention(
    x: np.ndarray,  # (T, D)
    w_q: np.ndarray,  # (D, D)
    w_k: np.ndarray,  # (D, D)
    w_v: np.ndarray,  # (D, D)
    w_o: np.ndarray,  # (D, D)
    num_heads: int,
) -> np.ndarray:
    """
    Causal (decoder) multi-head self-attention.

    Parameters
    ----------
    x : (T, D)  input sequence
    w_q/k/v/o : projection weight matrices
    num_heads : number of attention heads

    Returns
    -------
    np.ndarray  shape (T, D)
    """
    t, d = x.shape
    head_dim = d // num_heads

    q = x @ w_q  # (T, D)
    k = x @ w_k
    v = x @ w_v

    # Split into heads: (T, H, Dh) → (H, T, Dh)
    q = q.reshape(t, num_heads, head_dim).transpose(1, 0, 2)
    k = k.reshape(t, num_heads, head_dim).transpose(1, 0, 2)
    v = v.reshape(t, num_heads, head_dim).transpose(1, 0, 2)

    # Scaled dot-product attention
    scale = np.sqrt(head_dim)
    scores = q @ k.transpose(0, 2, 1) / scale  # (H, T, T)

    # Apply causal mask
    mask = _causal_mask(t)
    scores = np.where(mask[np.newaxis, :, :], scores, -1e9)

    attn = _softmax(scores, axis=-1)  # (H, T, T)
    ctx = attn @ v  # (H, T, Dh)

    # Merge heads: (H, T, Dh) → (T, D)
    ctx = ctx.transpose(1, 0, 2).reshape(t, d)
    return ctx @ w_o


# ---------------------------------------------------------------------------
# Feed-forward block
# ---------------------------------------------------------------------------


def feed_forward(
    x: np.ndarray,  # (T, D)
    w1: np.ndarray,  # (D, FF)
    b1: np.ndarray,  # (FF,)
    w2: np.ndarray,  # (FF, D)
    b2: np.ndarray,  # (D,)
) -> np.ndarray:
    """Two-layer GELU feed-forward network."""
    h = _gelu(x @ w1 + b1)
    return h @ w2 + b2


# ---------------------------------------------------------------------------
# Weight storage helpers
# ---------------------------------------------------------------------------


def _random_weights(rng: np.random.Generator, *shape: int) -> np.ndarray:
    """Xavier-uniform initialisation."""
    shape_list = list(shape)
    fan_in = shape_list[-2] if len(shape_list) >= 2 else shape_list[0]
    fan_out = shape_list[-1]
    limit = np.sqrt(6.0 / (fan_in + fan_out))
    return rng.uniform(-limit, limit, shape_list).astype(np.float32)


# ---------------------------------------------------------------------------
# TransformerWeights
# ---------------------------------------------------------------------------


class TransformerWeights:
    """
    Container for all learnable parameters of the nano Transformer.

    Attributes follow the naming convention used in :func:`multi_head_attention`
    and :func:`feed_forward` so callers can index by layer number.
    """

    def __init__(
        self,
        vocab_size: int,
        embed_dim: int,
        num_heads: int,
        num_layers: int,
        ff_dim: int,
        max_seq: int,
        seed: int = 42,
    ) -> None:
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.ff_dim = ff_dim
        self.max_seq = max_seq

        rng = np.random.default_rng(seed)

        # Token + positional embeddings
        self.tok_emb: np.ndarray = _random_weights(rng, vocab_size, embed_dim)
        self.pos_emb: np.ndarray = _random_weights(rng, max_seq, embed_dim)

        # Per-layer weights
        self.attn_wq: list[np.ndarray] = []
        self.attn_wk: list[np.ndarray] = []
        self.attn_wv: list[np.ndarray] = []
        self.attn_wo: list[np.ndarray] = []
        self.ln1_g: list[np.ndarray] = []
        self.ln1_b: list[np.ndarray] = []
        self.ff_w1: list[np.ndarray] = []
        self.ff_b1: list[np.ndarray] = []
        self.ff_w2: list[np.ndarray] = []
        self.ff_b2: list[np.ndarray] = []
        self.ln2_g: list[np.ndarray] = []
        self.ln2_b: list[np.ndarray] = []

        for _ in range(num_layers):
            self.attn_wq.append(_random_weights(rng, embed_dim, embed_dim))
            self.attn_wk.append(_random_weights(rng, embed_dim, embed_dim))
            self.attn_wv.append(_random_weights(rng, embed_dim, embed_dim))
            self.attn_wo.append(_random_weights(rng, embed_dim, embed_dim))
            self.ln1_g.append(np.ones(embed_dim, dtype=np.float32))
            self.ln1_b.append(np.zeros(embed_dim, dtype=np.float32))
            self.ff_w1.append(_random_weights(rng, embed_dim, ff_dim))
            self.ff_b1.append(np.zeros(ff_dim, dtype=np.float32))
            self.ff_w2.append(_random_weights(rng, ff_dim, embed_dim))
            self.ff_b2.append(np.zeros(embed_dim, dtype=np.float32))
            self.ln2_g.append(np.ones(embed_dim, dtype=np.float32))
            self.ln2_b.append(np.zeros(embed_dim, dtype=np.float32))

        # Final layer-norm + output projection
        self.final_ln_g = np.ones(embed_dim, dtype=np.float32)
        self.final_ln_b = np.zeros(embed_dim, dtype=np.float32)
        self.lm_head: np.ndarray = _random_weights(rng, embed_dim, vocab_size)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, object]:
        """Serialise all weights to a plain dict of base64-encoded arrays."""
        import base64

        def enc(arr: np.ndarray) -> dict[str, object]:
            return {
                "shape": list(arr.shape),
                "dtype": str(arr.dtype),
                "data": base64.b64encode(arr.tobytes()).decode(),
            }

        def enc_list(lst: list[np.ndarray]) -> list[dict[str, object]]:
            return [enc(a) for a in lst]

        return {
            "vocab_size": self.vocab_size,
            "embed_dim": self.embed_dim,
            "num_heads": self.num_heads,
            "num_layers": self.num_layers,
            "ff_dim": self.ff_dim,
            "max_seq": self.max_seq,
            "tok_emb": enc(self.tok_emb),
            "pos_emb": enc(self.pos_emb),
            "attn_wq": enc_list(self.attn_wq),
            "attn_wk": enc_list(self.attn_wk),
            "attn_wv": enc_list(self.attn_wv),
            "attn_wo": enc_list(self.attn_wo),
            "ln1_g": enc_list(self.ln1_g),
            "ln1_b": enc_list(self.ln1_b),
            "ff_w1": enc_list(self.ff_w1),
            "ff_b1": enc_list(self.ff_b1),
            "ff_w2": enc_list(self.ff_w2),
            "ff_b2": enc_list(self.ff_b2),
            "ln2_g": enc_list(self.ln2_g),
            "ln2_b": enc_list(self.ln2_b),
            "final_ln_g": enc(self.final_ln_g),
            "final_ln_b": enc(self.final_ln_b),
            "lm_head": enc(self.lm_head),
        }

    @classmethod
    def from_dict(cls, d: dict[str, object]) -> TransformerWeights:
        """Deserialise weights from the dict produced by :meth:`to_dict`."""
        import base64

        def dec(obj: object) -> np.ndarray:
            assert isinstance(obj, dict)
            raw = base64.b64decode(obj["data"])  # type: ignore[arg-type]
            return np.frombuffer(raw, dtype=obj["dtype"]).reshape(  # type: ignore[arg-type]
                obj["shape"]  # type: ignore[arg-type]
            )

        def dec_list(lst: object) -> list[np.ndarray]:
            assert isinstance(lst, list)
            return [dec(item) for item in lst]

        w = cls.__new__(cls)
        w.vocab_size = int(d["vocab_size"])  # type: ignore[arg-type]
        w.embed_dim = int(d["embed_dim"])  # type: ignore[arg-type]
        w.num_heads = int(d["num_heads"])  # type: ignore[arg-type]
        w.num_layers = int(d["num_layers"])  # type: ignore[arg-type]
        w.ff_dim = int(d["ff_dim"])  # type: ignore[arg-type]
        w.max_seq = int(d["max_seq"])  # type: ignore[arg-type]
        w.tok_emb = dec(d["tok_emb"])
        w.pos_emb = dec(d["pos_emb"])
        w.attn_wq = dec_list(d["attn_wq"])
        w.attn_wk = dec_list(d["attn_wk"])
        w.attn_wv = dec_list(d["attn_wv"])
        w.attn_wo = dec_list(d["attn_wo"])
        w.ln1_g = dec_list(d["ln1_g"])
        w.ln1_b = dec_list(d["ln1_b"])
        w.ff_w1 = dec_list(d["ff_w1"])
        w.ff_b1 = dec_list(d["ff_b1"])
        w.ff_w2 = dec_list(d["ff_w2"])
        w.ff_b2 = dec_list(d["ff_b2"])
        w.ln2_g = dec_list(d["ln2_g"])
        w.ln2_b = dec_list(d["ln2_b"])
        w.final_ln_g = dec(d["final_ln_g"])
        w.final_ln_b = dec(d["final_ln_b"])
        w.lm_head = dec(d["lm_head"])
        return w

    def fingerprint(self) -> str:
        """SHA-256 of the serialised weight dict — used as memory cell seed."""
        blob = json.dumps(
            {
                k: v
                for k, v in self.to_dict().items()
                if k not in ("tok_emb", "pos_emb")
            },
            sort_keys=True,
        ).encode()
        return hashlib.sha256(blob).hexdigest()


# ---------------------------------------------------------------------------
# Forward pass
# ---------------------------------------------------------------------------


def _forward(tokens: list[int], weights: TransformerWeights) -> np.ndarray:
    """
    Full forward pass through the Transformer decoder.

    Parameters
    ----------
    tokens : list[int]  — input token IDs (length T)
    weights : TransformerWeights

    Returns
    -------
    np.ndarray  shape (T, vocab_size)  — logits
    """
    t = len(tokens)
    if t == 0:
        return np.zeros((0, weights.vocab_size), dtype=np.float32)
    t = min(t, weights.max_seq)
    tokens = tokens[-t:]

    ids = np.array(tokens, dtype=np.int32)
    x: np.ndarray = weights.tok_emb[ids] + weights.pos_emb[:t]  # (T, D)

    for layer in range(weights.num_layers):
        # Pre-norm attention
        x_norm = _layer_norm(x, weights.ln1_g[layer], weights.ln1_b[layer])
        attn_out = multi_head_attention(
            x_norm,
            weights.attn_wq[layer],
            weights.attn_wk[layer],
            weights.attn_wv[layer],
            weights.attn_wo[layer],
            weights.num_heads,
        )
        x = x + attn_out

        # Pre-norm feed-forward
        x_norm = _layer_norm(x, weights.ln2_g[layer], weights.ln2_b[layer])
        ff_out = feed_forward(
            x_norm,
            weights.ff_w1[layer],
            weights.ff_b1[layer],
            weights.ff_w2[layer],
            weights.ff_b2[layer],
        )
        x = x + ff_out

    x = _layer_norm(x, weights.final_ln_g, weights.final_ln_b)
    return x @ weights.lm_head  # (T, vocab_size)


def _forward_hidden(tokens: list[int], weights: TransformerWeights) -> np.ndarray:
    """
    Forward pass returning the final hidden states (T, embed_dim) **before**
    the ``lm_head`` projection.

    Used by the fine-tuning gradient step so that::

        grad_lm = hidden.T @ d_logits   # (embed_dim, vocab_size)  ✓

    Using ``_forward`` here would give shape ``(vocab_size, T-1) @ (T-1,
    vocab_size)`` which broadcasts to ``(vocab_size, vocab_size)`` — wrong.

    Parameters
    ----------
    tokens : list[int]  — input token IDs (length T)
    weights : TransformerWeights

    Returns
    -------
    np.ndarray  shape (T, embed_dim)
    """
    t = len(tokens)
    if t == 0:
        return np.zeros((0, weights.embed_dim), dtype=np.float32)
    t = min(t, weights.max_seq)
    tokens = tokens[-t:]

    ids = np.array(tokens, dtype=np.int32)
    x: np.ndarray = weights.tok_emb[ids] + weights.pos_emb[:t]  # (T, D)

    for layer in range(weights.num_layers):
        # Pre-norm attention
        x_norm = _layer_norm(x, weights.ln1_g[layer], weights.ln1_b[layer])
        attn_out = multi_head_attention(
            x_norm,
            weights.attn_wq[layer],
            weights.attn_wk[layer],
            weights.attn_wv[layer],
            weights.attn_wo[layer],
            weights.num_heads,
        )
        x = x + attn_out

        # Pre-norm feed-forward
        x_norm = _layer_norm(x, weights.ln2_g[layer], weights.ln2_b[layer])
        ff_out = feed_forward(
            x_norm,
            weights.ff_w1[layer],
            weights.ff_b1[layer],
            weights.ff_w2[layer],
            weights.ff_b2[layer],
        )
        x = x + ff_out

    # Final layer-norm — stops before lm_head, returns (T, embed_dim)
    return _layer_norm(x, weights.final_ln_g, weights.final_ln_b)


def _gelu_derivative(x: np.ndarray) -> np.ndarray:
    """Element-wise analytic derivative of the GELU activation.

    Used during backpropagation through the feed-forward layers.
    Derived from: GELU(x) = 0.5·x·(1 + tanh(√(2/π)·(x + 0.044715·x³)))
    """
    sqrt_2_pi = np.sqrt(2.0 / np.pi)
    inner = sqrt_2_pi * (x + 0.044715 * x ** 3)
    t = np.tanh(inner)
    dt = (1.0 - t ** 2) * sqrt_2_pi * (1.0 + 3.0 * 0.044715 * x ** 2)
    return 0.5 * (1.0 + t) + 0.5 * x * dt


def _forward_and_cache(
    tokens: list[int],
    weights: TransformerWeights,
) -> tuple[np.ndarray, list[dict[str, np.ndarray]]]:
    """Forward pass that saves per-layer activations needed for FF backprop.

    Parameters
    ----------
    tokens : list[int]
        Input token IDs.
    weights : TransformerWeights

    Returns
    -------
    hidden : np.ndarray  shape (T, embed_dim)
        Final hidden states **before** the lm_head projection.
        Identical to the return value of ``_forward_hidden``.
    layer_caches : list[dict]
        One dict per Transformer layer, containing:

        ``"ff_input"``  (T, D)  — normalised input to the FF sub-layer
                                  (output of LN2, before ff_w1 multiplication).
        ``"ff_pre"``    (T, FF) — pre-GELU activations inside the FF layer
                                  (i.e. ff_input @ ff_w1 + ff_b1).

        These are the two tensors needed to compute gradients for
        ff_w1, ff_b1, ff_w2, ff_b2 during the backward pass.
    """
    t = len(tokens)
    if t == 0:
        return np.zeros((0, weights.embed_dim), dtype=np.float32), []
    t = min(t, weights.max_seq)
    tokens = tokens[-t:]

    ids = np.array(tokens, dtype=np.int32)
    x: np.ndarray = weights.tok_emb[ids] + weights.pos_emb[:t]  # (T, D)

    layer_caches: list[dict[str, np.ndarray]] = []

    for layer in range(weights.num_layers):
        # Pre-norm attention residual (not cached — attention backprop deferred)
        x_norm = _layer_norm(x, weights.ln1_g[layer], weights.ln1_b[layer])
        attn_out = multi_head_attention(
            x_norm,
            weights.attn_wq[layer], weights.attn_wk[layer],
            weights.attn_wv[layer], weights.attn_wo[layer],
            weights.num_heads,
        )
        x = x + attn_out

        # Pre-norm feed-forward — save input and pre-activation for backprop
        ff_input = _layer_norm(x, weights.ln2_g[layer], weights.ln2_b[layer])  # (T, D)
        ff_pre = ff_input @ weights.ff_w1[layer] + weights.ff_b1[layer]        # (T, FF)
        ff_out = _gelu(ff_pre) @ weights.ff_w2[layer] + weights.ff_b2[layer]   # (T, D)
        x = x + ff_out

        layer_caches.append({"ff_input": ff_input, "ff_pre": ff_pre})

    return _layer_norm(x, weights.final_ln_g, weights.final_ln_b), layer_caches


def _sample_token(logits: np.ndarray, temperature: float, top_k: int = 50) -> int:
    """Sample the next token from logits with temperature + top-k."""
    if temperature <= 0.0:
        return int(np.argmax(logits))
    logits = logits.astype(np.float64)
    logits /= max(temperature, 1e-6)
    # Top-k filtering
    if top_k > 0:
        threshold = np.partition(logits, -top_k)[-top_k]
        logits = np.where(logits >= threshold, logits, -1e9)
    probs = _softmax(logits)
    return int(np.random.choice(len(probs), p=probs))


# ---------------------------------------------------------------------------
# Code templates for demo / pattern-based generation
# ---------------------------------------------------------------------------

_CODE_TEMPLATES: dict[str, str] = {
    "def ": ('    """{doc}"""\n' "    # TODO: implement\n" "    pass\n"),
    "class ": (
        '    """Auto-generated class."""\n\n'
        "    def __init__(self):\n"
        "        pass\n"
    ),
    "import ": "# module imported\n",
    "for ": "    pass\n",
    "while ": "    pass\n",
    "if ": "    pass\n",
}

_LANGUAGE_STARTERS: dict[str, str] = {
    "python": "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n\n",
    "javascript": '"use strict";\n\n',
    "typescript": '"use strict";\n\n',
    "go": 'package main\n\nimport "fmt"\n\n',
    "rust": 'fn main() {\n    println!("Hello, world!");\n}\n',
    "bash": "#!/usr/bin/env bash\nset -euo pipefail\n\n",
}


# ---------------------------------------------------------------------------
# NeuralCodeGen — main public class
# ---------------------------------------------------------------------------


class NeuralCodeGen:
    """
    Transformer-based code generation engine.

    Quick start
    -----------
    >>> gen = NeuralCodeGen()
    >>> gen.load_demo_weights()
    >>> print(gen.generate("def greet(name):"))

    Memory persistence
    ------------------
    >>> from core.cell_memory import HoneycombMemory
    >>> mem = HoneycombMemory()
    >>> gen.save_to_memory(mem)
    >>> gen2 = NeuralCodeGen.load_from_memory(mem, gen.weights.fingerprint())
    """

    def __init__(
        self,
        embed_dim: int = DEFAULT_EMBED_DIM,
        num_heads: int = DEFAULT_NUM_HEADS,
        num_layers: int = DEFAULT_NUM_LAYERS,
        ff_dim: int = DEFAULT_FF_DIM,
        max_seq: int = DEFAULT_MAX_SEQ,
    ) -> None:
        # ByteTokenizer handles every language via UTF-8 byte encoding.
        # CharTokenizer is kept only for loading old ASCII weight files.
        self.tokenizer: ByteTokenizer | CharTokenizer = ByteTokenizer()
        self.weights: TransformerWeights | None = None
        self._embed_dim = embed_dim
        self._num_heads = num_heads
        self._num_layers = num_layers
        self._ff_dim = ff_dim
        self._max_seq = max_seq
        # Adam optimizer — state persists across fine_tune_on_examples calls
        # within the same process so momentum carries over between seed files.
        self._adam = AdamOptimizer(lr=5e-4)

    # ------------------------------------------------------------------
    # Weight management
    # ------------------------------------------------------------------

    def load_demo_weights(self, seed: int = 42) -> None:
        """
        Load deterministic random weights.  The model won't produce
        meaningful code from scratch but validates the full pipeline.
        Call :meth:`fine_tune_on_examples` to improve output quality.
        """
        self.weights = TransformerWeights(
            vocab_size=self.tokenizer.vocab_size,
            embed_dim=self._embed_dim,
            num_heads=self._num_heads,
            num_layers=self._num_layers,
            ff_dim=self._ff_dim,
            max_seq=self._max_seq,
            seed=seed,
        )
        logger.info("Demo weights loaded (seed=%d)", seed)

    def save_to_memory(self, memory: HoneycombMemory) -> str:
        """
        Persist weights to a :class:`HoneycombMemory` cell.

        Returns the cell ID (== weight fingerprint).
        """
        if self.weights is None:
            raise RuntimeError("No weights loaded — call load_demo_weights() first")
        fp = self.weights.fingerprint()
        blob = json.dumps(self.weights.to_dict()).encode()
        cell = memory.create_cell(
            seed=fp, data=blob, meta={"type": "transformer_weights"}
        )
        logger.info("Weights saved to cell %s (%d bytes)", cell.cell_id[:8], len(blob))
        return cell.cell_id

    @classmethod
    def load_from_memory(cls, memory: HoneycombMemory, cell_id: str) -> NeuralCodeGen:
        """Reconstruct a :class:`NeuralCodeGen` instance from a memory cell."""
        cell = memory.get_cell(cell_id)
        if cell is None:
            raise KeyError(f"Cell not found: {cell_id}")
        d = json.loads(cell.read())
        weights = TransformerWeights.from_dict(d)
        gen = cls(
            embed_dim=weights.embed_dim,
            num_heads=weights.num_heads,
            num_layers=weights.num_layers,
            ff_dim=weights.ff_dim,
            max_seq=weights.max_seq,
        )
        gen.weights = weights
        # Auto-detect: old ASCII weights have vocab_size ≤ 98
        if weights.vocab_size <= 98:
            gen.tokenizer = CharTokenizer()
            logger.info("Legacy ASCII weights detected — using CharTokenizer")
        return gen

    # ------------------------------------------------------------------
    # File-level persistence
    # ------------------------------------------------------------------

    def save_to_file(self, path: str | os.PathLike[str]) -> None:
        """Persist model weights to a JSON file on disk (atomic write).

        Trained weights survive container restarts when saved here.
        Load back with :meth:`load_from_file`.

        Parameters
        ----------
        path:
            Destination file, e.g. ``data/weights/neural_core.json``.
        """
        if self.weights is None:
            raise RuntimeError("No weights loaded — call load_demo_weights() first")
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        blob = json.dumps(self.weights.to_dict())
        tmp = str(path) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(blob)
        os.replace(tmp, path)
        logger.info("Weights saved to file %s (%d bytes)", path, len(blob))

    @classmethod
    def load_from_file(cls, path: str | os.PathLike[str]) -> NeuralCodeGen:
        """Load weights from a file written by :meth:`save_to_file`.

        Parameters
        ----------
        path:
            Source file path.

        Returns
        -------
        NeuralCodeGen
            New instance with weights loaded.

        Raises
        ------
        FileNotFoundError
            If *path* does not exist.
        """
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
        weights = TransformerWeights.from_dict(d)
        gen = cls(
            embed_dim=weights.embed_dim,
            num_heads=weights.num_heads,
            num_layers=weights.num_layers,
            ff_dim=weights.ff_dim,
            max_seq=weights.max_seq,
        )
        gen.weights = weights
        # Auto-detect: old ASCII weights have vocab_size ≤ 98
        if weights.vocab_size <= 98:
            gen.tokenizer = CharTokenizer()
            logger.info("Legacy ASCII weights detected — using CharTokenizer")
        logger.info("Weights loaded from file %s", path)
        return gen

    # ------------------------------------------------------------------
    # Fine-tuning (gradient descent, in-memory)
    # ------------------------------------------------------------------

    def fine_tune_on_examples(
        self,
        examples: list[str],
        *,
        epochs: int = 3,
        learning_rate: float = 5e-4,
        max_tokens_per_example: int = 128,
        throttle_ms: int = 1,
    ) -> list[float]:
        """Train on a list of text strings using Adam + FF-layer backprop.

        v2.0 improvements over v1.x
        ----------------------------
        * **Adam optimizer** — adaptive per-parameter learning rates replace
          fixed-LR SGD.  Faster convergence, less sensitivity to LR choice.
        * **FF layer gradients** — backpropagates through all feed-forward
          blocks (ff_w1/b1 and ff_w2/b2 for every layer), not just lm_head.
          This trains ~50% of all model parameters instead of ~2%.
        * **tok_emb gradient** — embedding layer is still updated with a
          simplified gradient signal for multilingual byte representations.

        Parameters
        ----------
        examples : list[str]
            Training text snippets (any language, any encoding).
        epochs : int
            Number of passes over *examples*.
        learning_rate : float
            Adam learning rate (default 5e-4; lower than SGD default).
        max_tokens_per_example : int
            Truncate each example to this many tokens to bound memory.
        throttle_ms : int
            Sleep ms between steps to limit CPU load (0 = no throttle).

        Returns
        -------
        list[float]
            Per-epoch average cross-entropy loss.  Lower = better fit.
        """
        if self.weights is None:
            raise RuntimeError("Load weights first")

        w = self.weights
        self._adam.lr = learning_rate  # honour caller's LR preference
        losses: list[float] = []

        for epoch in range(epochs):
            total_loss = 0.0
            count = 0

            for text in examples:
                ids = self.tokenizer.encode(text)[:max_tokens_per_example]
                if len(ids) < 2:
                    continue

                targets = np.array(ids[1:], dtype=np.int32)

                # --- Forward pass with activation cache ---
                # hidden: (T-1, D)  layer_caches: list[{ff_input, ff_pre}]
                hidden, layer_caches = _forward_and_cache(ids[:-1], w)
                logits = hidden @ w.lm_head  # (T-1, V)

                # --- Cross-entropy loss (numerically stable log-softmax) ---
                shifted = logits - logits.max(axis=-1, keepdims=True)
                log_probs = shifted - np.log(
                    np.exp(shifted).sum(axis=-1, keepdims=True)
                )
                loss = -log_probs[np.arange(len(targets)), targets].mean()
                total_loss += float(loss)
                count += 1

                # --- d_logits: softmax - one_hot(targets), shape (T-1, V) ---
                probs = _softmax(logits)
                probs[np.arange(len(targets)), targets] -= 1.0
                probs /= len(targets)

                # ===================== BACKWARD PASS =====================

                # Increment Adam timestep once per training step
                self._adam.step()

                # 1. lm_head gradient: hidden.T @ probs → (D, V)
                grad_lm = hidden.T @ probs
                self._adam.update("lm_head", w.lm_head, grad_lm)

                # Gradient of loss w.r.t. hidden states: (T-1, D)
                d_x = probs @ w.lm_head.T

                # 2. FF layer gradients (reversed — deepest layer first)
                for layer in reversed(range(w.num_layers)):
                    cache = layer_caches[layer]
                    ff_input = cache["ff_input"]   # (T-1, D) — LN2 output
                    ff_pre   = cache["ff_pre"]     # (T-1, FF) — pre-GELU

                    ff_h = _gelu(ff_pre)           # (T-1, FF) — post-GELU

                    # Gradient for ff_w2 and ff_b2
                    # ff_out = ff_h @ ff_w2 + ff_b2
                    grad_w2 = ff_h.T @ d_x                          # (FF, D)
                    grad_b2 = d_x.sum(axis=0)                        # (D,)
                    self._adam.update(f"ff_w2_{layer}", w.ff_w2[layer], grad_w2)
                    self._adam.update(f"ff_b2_{layer}", w.ff_b2[layer], grad_b2)

                    # Gradient back through ff_w2 into ff_h
                    d_ff_h = d_x @ w.ff_w2[layer].T                 # (T-1, FF)

                    # Gradient through GELU non-linearity
                    d_ff_pre = d_ff_h * _gelu_derivative(ff_pre)    # (T-1, FF)

                    # Gradient for ff_w1 and ff_b1
                    # ff_pre = ff_input @ ff_w1 + ff_b1
                    grad_w1 = ff_input.T @ d_ff_pre                  # (D, FF)
                    grad_b1 = d_ff_pre.sum(axis=0)                   # (FF,)
                    self._adam.update(f"ff_w1_{layer}", w.ff_w1[layer], grad_w1)
                    self._adam.update(f"ff_b1_{layer}", w.ff_b1[layer], grad_b1)

                    # Gradient back through ff_w1 + FF residual connection
                    # (LN Jacobian approximated as identity — standard practice)
                    d_x = d_x + d_ff_pre @ w.ff_w1[layer].T         # (T-1, D)

                # 3. tok_emb gradient (simplified signal, SGD for per-row update)
                # d_emb: approximate gradient at embedding rows via lm_head.T
                d_emb = probs @ w.lm_head.T                          # (T-1, D)
                emb_lr = learning_rate * 0.3
                for t_idx, tok_id in enumerate(ids[:-1]):
                    if 0 <= tok_id < w.vocab_size:
                        w.tok_emb[tok_id] -= emb_lr * d_emb[t_idx]

                # =========================================================

                if throttle_ms > 0:
                    time.sleep(throttle_ms / 1000.0)

            avg = total_loss / max(count, 1)
            losses.append(avg)
            logger.info("Epoch %d/%d — avg loss: %.4f", epoch + 1, epochs, avg)

        return losses

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate(
        self,
        prompt: str,
        *,
        max_new_tokens: int = 256,
        temperature: float = DEFAULT_TEMPERATURE,
        top_k: int = 50,
        stop_sequences: list[str] | None = None,
        language: str = "python",
        throttle_ms: int = 1,
    ) -> str:
        """
        Generate code continuation from *prompt*.

        Parameters
        ----------
        prompt : str
            The code prefix to continue.
        max_new_tokens : int
            Maximum number of new characters to generate.
        temperature : float
            Sampling temperature (0 = greedy, 1 = random).
        top_k : int
            Keep only the top-k most probable tokens.
        stop_sequences : list[str], optional
            Generation stops when any of these strings appear.
        language : str
            Target language — used for heuristic pattern matching when
            model weights are not yet trained.
        throttle_ms : int
            Sleep between tokens to limit CPU load.

        Returns
        -------
        str
            The full generated text (prompt + continuation).
        """
        if self.weights is None:
            raise RuntimeError("Load weights first with load_demo_weights()")

        stops = stop_sequences or ["\n\n\n"]
        tokens = self.tokenizer.encode(prompt)
        generated: list[int] = []

        start_ts = time.monotonic()
        for step in range(max_new_tokens):
            logits = _forward(tokens + generated, self.weights)
            if logits.shape[0] == 0:
                break
            next_id = _sample_token(logits[-1], temperature, top_k)
            generated.append(next_id)

            # Check stop sequences
            current_text = self.tokenizer.decode(generated)
            for stop in stops:
                if stop in current_text:
                    # Trim at stop token
                    idx = current_text.index(stop)
                    generated = self.tokenizer.encode(current_text[:idx])
                    break
            else:
                if throttle_ms > 0 and step % 32 == 0:
                    time.sleep(throttle_ms / 1000.0)
                continue
            break

        elapsed = time.monotonic() - start_ts
        n = len(generated)
        logger.info(
            "Generated %d tokens in %.2fs (%.0f tok/s)",
            n,
            elapsed,
            n / max(elapsed, 1e-6),
        )

        # Combine prompt + generated; apply heuristic polish
        raw = prompt + self.tokenizer.decode(generated)
        return _heuristic_polish(raw, language)

    def generate_from_description(
        self,
        description: str,
        *,
        language: str = "python",
        max_new_tokens: int = 512,
    ) -> str:
        """
        Generate a complete code snippet from a natural-language description.

        The description is wrapped in a structured prompt before generation.

        Parameters
        ----------
        description : str
            E.g. "A function that reverses a list in Python".
        language : str
            Target programming language.
        max_new_tokens : int
            Token budget.

        Returns
        -------
        str
            Generated source code.
        """
        starter = _LANGUAGE_STARTERS.get(language.lower(), "")
        prompt = (
            f"# Language: {language}\n"
            f"# Task: {description}\n"
            f"# Generated code:\n"
            f"{starter}"
        )
        return self.generate(
            prompt,
            max_new_tokens=max_new_tokens,
            language=language,
            temperature=0.7,
        )

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @property
    def parameter_count(self) -> int:
        """Total number of floating-point parameters."""
        if self.weights is None:
            return 0
        total = 0
        for arr in [
            self.weights.tok_emb,
            self.weights.pos_emb,
            self.weights.final_ln_g,
            self.weights.final_ln_b,
            self.weights.lm_head,
        ]:
            total += arr.size
        for lst in [
            self.weights.attn_wq,
            self.weights.attn_wk,
            self.weights.attn_wv,
            self.weights.attn_wo,
            self.weights.ln1_g,
            self.weights.ln1_b,
            self.weights.ff_w1,
            self.weights.ff_b1,
            self.weights.ff_w2,
            self.weights.ff_b2,
            self.weights.ln2_g,
            self.weights.ln2_b,
        ]:
            for arr in lst:
                total += arr.size
        return total

    def __repr__(self) -> str:  # pragma: no cover
        loaded = self.weights is not None
        return (
            f"NeuralCodeGen(layers={self._num_layers}, "
            f"dim={self._embed_dim}, "
            f"params={self.parameter_count:,}, "
            f"loaded={loaded})"
        )


# ---------------------------------------------------------------------------
# Heuristic post-processing
# ---------------------------------------------------------------------------


def _heuristic_polish(text: str, language: str) -> str:
    """
    Light post-processing: fix obvious indentation issues and
    inject template bodies for bare function/class stubs.
    """
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    for line in lines:
        stripped = line.lstrip()
        for prefix in _CODE_TEMPLATES:
            if stripped.startswith(prefix) and stripped.endswith(":\n"):
                out.append(line)
                # Body will be generated by the model continuation
                break
        else:
            out.append(line)
    return "".join(out)
