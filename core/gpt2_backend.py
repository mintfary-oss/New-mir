"""
GPT-2 Backend
=============
Powers the Chat tab with real pre-trained GPT-2 weights instead of the
random-initialised nano-model used by NeuralCodeGen.

GPT-2 was trained on 40 GB of diverse internet text and knows English well,
plus many other popular languages (Russian, French, Spanish, German, Chinese,
Arabic, Japanese …) to varying degrees.  For the best multilingual results
set the environment variable ``NEW_MIR_CHAT_MODEL`` to a larger or
language-specific model (examples below), but the default ``"gpt2"`` works
without configuration:

    NEW_MIR_CHAT_MODEL=gpt2                     # 117 M  English-focused
    NEW_MIR_CHAT_MODEL=gpt2-medium              # 345 M  better quality
    NEW_MIR_CHAT_MODEL=sberbank-ai/rugpt3small  # Russian GPT-3 small
    NEW_MIR_CHAT_MODEL=bigscience/bloom-560m    # 559 M  46 languages

Interface compatibility with NeuralCodeGen
------------------------------------------
ChatEngine only calls these on the model object:

    model.weights          — None when not loaded, truthy once loaded
    model.tokenizer        — .encode(str)->list[int], .decode(list[int])->str
    model._max_seq         — int, context window length
    model.load_demo_weights(seed)
    model.generate(prompt, *, max_new_tokens, temperature, throttle_ms,
                   stop_sequences, top_k, language) -> str
    model.fine_tune_on_examples(examples, *, epochs, ...) -> list[float]
    model.parameter_count  — int property

All of those are provided here with the exact same signatures.
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any

logger = logging.getLogger("new-mir.gpt2")

# ---------------------------------------------------------------------------
# Tokenizer wrapper
# ---------------------------------------------------------------------------


class _HFTokenizerWrapper:
    """Adapts a HuggingFace tokenizer to the CharTokenizer interface."""

    def __init__(self, hf_tokenizer: Any) -> None:
        self._tok = hf_tokenizer

    @property
    def vocab_size(self) -> int:
        return int(self._tok.vocab_size)

    def encode(self, text: str) -> list[int]:
        """Convert a string to a list of BPE token IDs."""
        return self._tok.encode(text)  # type: ignore[no-any-return]

    def decode(self, ids: list[int]) -> str:
        """Convert a list of token IDs back to a string."""
        return self._tok.decode(ids, skip_special_tokens=True)  # type: ignore[no-any-return]


# ---------------------------------------------------------------------------
# GPT2Backend
# ---------------------------------------------------------------------------


class GPT2Backend:
    """
    HuggingFace-powered GPT-2 text generation backend.

    Drop-in replacement for :class:`~core.neural_core.NeuralCodeGen` for the
    Chat tab.  Uses real GPT-2 weights for coherent, multilingual text.

    Parameters
    ----------
    model_name : str
        HuggingFace model identifier.  Read from the ``NEW_MIR_CHAT_MODEL``
        environment variable; falls back to ``"gpt2"``.
    """

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        self.model_name: str = model_name or os.environ.get(
            "NEW_MIR_CHAT_MODEL", "gpt2"
        )

        # Public interface expected by ChatEngine
        self.weights: Any = None  # None = not loaded
        self.tokenizer: Any = None
        self._max_seq: int = 1024  # GPT-2 default context

        # Private
        self._model: Any = None
        self._hf_tokenizer: Any = None

    # ------------------------------------------------------------------
    # Weight loading
    # ------------------------------------------------------------------

    def load_demo_weights(self, seed: int = 42) -> None:  # noqa: ARG002
        """
        Download (once) and load GPT-2 weights from HuggingFace.

        The ``seed`` argument is accepted for API compatibility but ignored.

        Raises
        ------
        ImportError
            If ``torch`` or ``transformers`` are not installed.
        """
        try:
            import torch  # type: ignore[import-untyped]
            from transformers import (  # type: ignore[import-untyped]
                AutoModelForCausalLM,
                AutoTokenizer,
            )
        except ImportError as exc:
            raise ImportError(
                "GPT-2 backend requires 'torch' and 'transformers'.\n"
                "Install:  pip install torch transformers"
            ) from exc

        logger.info("Loading GPT-2 model '%s' …", self.model_name)
        t0 = time.monotonic()

        hf_tok = AutoTokenizer.from_pretrained(self.model_name)
        if hf_tok.pad_token is None:
            hf_tok.pad_token = hf_tok.eos_token

        # Determine context window from model config if possible
        try:
            cfg = hf_tok.model_max_length
            if isinstance(cfg, int) and 128 <= cfg <= 32_768:
                self._max_seq = cfg
        except Exception:  # noqa: BLE001
            pass

        model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
        )
        model.eval()

        self._hf_tokenizer = hf_tok
        self._model = model
        self.tokenizer = _HFTokenizerWrapper(hf_tok)
        self.weights = object()  # non-None sentinel

        logger.info(
            "GPT-2 '%s' ready — %d params, %.1fs",
            self.model_name,
            self.parameter_count,
            time.monotonic() - t0,
        )

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate(
        self,
        prompt: str,
        *,
        max_new_tokens: int = 256,
        temperature: float = 0.8,
        top_k: int = 50,
        stop_sequences: list[str] | None = None,
        language: str = "python",  # noqa: ARG002  — compat only
        throttle_ms: int = 1,  # noqa: ARG002  — compat only
    ) -> str:
        """
        Generate a text continuation from *prompt*.

        Returns
        -------
        str
            Always ``prompt + continuation`` so callers can extract the new
            text via ``result[len(prompt):]``.
        """
        if self._model is None or self._hf_tokenizer is None:
            raise RuntimeError("GPT-2 not loaded — call load_demo_weights()")

        import torch  # type: ignore[import-untyped]

        stops = stop_sequences or ["\n\n\n"]

        # Tokenise, truncating if necessary to leave room for new tokens
        budget = max(self._max_seq - max_new_tokens, 64)
        input_ids = self._hf_tokenizer.encode(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=budget,
        )
        prompt_len = input_ids.shape[1]

        gen_kwargs: dict[str, Any] = {
            "max_new_tokens": max_new_tokens,
            "pad_token_id": self._hf_tokenizer.eos_token_id,
        }
        if temperature > 0.0:
            gen_kwargs["do_sample"] = True
            gen_kwargs["temperature"] = float(temperature)
            gen_kwargs["top_k"] = int(top_k)
        else:
            gen_kwargs["do_sample"] = False

        with torch.no_grad():
            output = self._model.generate(input_ids, **gen_kwargs)

        new_ids: list[int] = output[0][prompt_len:].tolist()
        if not new_ids:
            return prompt

        continuation: str = self._hf_tokenizer.decode(new_ids, skip_special_tokens=True)

        # Trim at first stop-sequence occurrence
        for stop in stops:
            if stop in continuation:
                continuation = continuation[: continuation.index(stop)]
                break

        return prompt + continuation

    # ------------------------------------------------------------------
    # Fine-tuning (no-op for now — GPT-2 weights are read-only)
    # ------------------------------------------------------------------

    def fine_tune_on_examples(
        self,
        examples: list[str],  # noqa: ARG002
        *,
        epochs: int = 1,
        learning_rate: float = 1e-3,  # noqa: ARG002
        max_tokens_per_example: int = 128,  # noqa: ARG002
        throttle_ms: int = 1,  # noqa: ARG002
    ) -> list[float]:
        """No-op — GPT-2 weights are pre-trained and kept read-only here."""
        return [0.0] * max(epochs, 1)

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @property
    def parameter_count(self) -> int:
        if self._model is None:
            return 0
        return sum(int(p.numel()) for p in self._model.parameters())

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"GPT2Backend(model={self.model_name!r}, "
            f"params={self.parameter_count:,}, "
            f"loaded={self.weights is not None})"
        )
