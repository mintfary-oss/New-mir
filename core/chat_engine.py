"""
Chat Engine
===========
Manages multi-turn conversations with the NeuralCodeGen model.

Key design decisions
--------------------
* **Unbounded generation** — the model keeps producing tokens until
  the task is complete (or the user presses Stop).  There is no hard
  token ceiling; the engine chunks output and streams it via SSE.

* **Stop / Continue** — a ``ChatSession`` carries a threading.Event
  (``_stop_event``).  The generator loop checks it every *CHUNK_TOKENS*
  tokens.  When set the generator suspends and the session enters
  ``PAUSED`` state.  ``continue_session()`` clears the event and resumes
  from the exact token position where it stopped.

* **Conversation history** — each user/assistant turn is appended to
  ``session.history`` so the model has full context on every new turn.

* **SSE stream format** — each chunk is a JSON line::

      data: {"type": "token", "text": "...", "done": false}\n\n
      data: {"type": "done",  "text": "",   "done": true}\n\n
      data: {"type": "error", "text": "...", "done": true}\n\n

SSE ``[DONE]`` sentinel is sent at the end so the frontend knows
generation is complete without polling.
"""

from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from collections.abc import Generator
from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.neural_core import NeuralCodeGen

logger = logging.getLogger("new-mir.chat")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

CHUNK_TOKENS: int = 32  # tokens generated between stop-flag checks
MAX_HISTORY_TURNS: int = 50  # max turns kept in memory per session
DEFAULT_MAX_TOKENS: int = 4096  # default per-turn generation budget
TEMPERATURE: float = 0.85  # default sampling temperature


# ---------------------------------------------------------------------------
# Session state machine
# ---------------------------------------------------------------------------


class SessionState(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    DONE = "done"
    ERROR = "error"


@dataclass
class ChatMessage:
    role: str  # "user" | "assistant" | "system"
    content: str
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, object]:
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }


@dataclass
class ChatSession:
    """One conversation session — lives in RAM until the process restarts."""

    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:16])
    history: list[ChatMessage] = field(default_factory=list)
    state: SessionState = SessionState.IDLE
    created_at: float = field(default_factory=time.time)

    # Internal generation bookkeeping
    _pending_prompt: str = field(default="", repr=False)
    _generated_so_far: str = field(default="", repr=False)
    _stop_event: threading.Event = field(default_factory=threading.Event, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def add_message(self, role: str, content: str) -> None:
        self.history.append(ChatMessage(role=role, content=content))
        # Trim to keep memory bounded
        if len(self.history) > MAX_HISTORY_TURNS * 2:
            # Keep system prompt if present, then last N turns
            system = [m for m in self.history if m.role == "system"]
            rest = [m for m in self.history if m.role != "system"]
            self.history = system + rest[-MAX_HISTORY_TURNS * 2 :]

    def to_dict(self) -> dict[str, object]:
        return {
            "session_id": self.session_id,
            "state": self.state.value,
            "turns": len([m for m in self.history if m.role == "user"]),
            "created_at": self.created_at,
        }

    def _build_prompt(self, new_user_message: str) -> str:
        """Concatenate history into a single string prompt for the model."""
        parts: list[str] = []
        # System preamble
        parts.append(
            "Ты — New-mir, умная нейросеть-помощник.\n"
            "Ты пишешь код, книги, статьи и отвечаешь на любые вопросы.\n"
            "Пиши ровно столько, сколько нужно для полного выполнения задачи.\n"
            "---\n"
        )
        for msg in self.history[-MAX_HISTORY_TURNS:]:
            if msg.role == "user":
                parts.append(f"Пользователь: {msg.content}\n")
            elif msg.role == "assistant":
                parts.append(f"New-mir: {msg.content}\n")
        parts.append(f"Пользователь: {new_user_message}\nNew-mir:")
        return "".join(parts)


# ---------------------------------------------------------------------------
# ChatEngine
# ---------------------------------------------------------------------------


class ChatEngine:
    """
    Manages all active chat sessions and drives the generation loop.

    Parameters
    ----------
    neural_gen : NeuralCodeGen
        The shared code-generation model.
    """

    def __init__(self, neural_gen: NeuralCodeGen) -> None:
        self._gen = neural_gen
        self._sessions: dict[str, ChatSession] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Session lifecycle
    # ------------------------------------------------------------------

    def new_session(self) -> ChatSession:
        session = ChatSession()
        with self._lock:
            self._sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> ChatSession | None:
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[dict[str, object]]:
        return [s.to_dict() for s in self._sessions.values()]

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    def generate_stream(
        self,
        session_id: str,
        user_message: str,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = TEMPERATURE,
    ) -> Generator[str, None, None]:
        """
        Yield SSE-formatted text chunks for a new user message.

        Yields ``data: <json>\\n\\n`` strings suitable for
        ``StreamingResponse(media_type="text/event-stream")``.

        The generator respects the session's ``_stop_event``; if set it
        suspends and yields a ``paused`` event so the caller can close the
        HTTP response while preserving session state.
        """
        session = self._sessions.get(session_id)
        if session is None:
            yield _sse({"type": "error", "text": "Session not found", "done": True})
            return

        with session._lock:
            if session.state == SessionState.RUNNING:
                yield _sse(
                    {
                        "type": "error",
                        "text": "Already running — stop first",
                        "done": True,
                    }
                )
                return

            session.state = SessionState.RUNNING
            session._stop_event.clear()

            # Build prompt — include any previously paused partial response
            if session._generated_so_far:
                # Resuming: prepend what was already written
                prompt = (
                    session._build_prompt(session._pending_prompt)
                    + session._generated_so_far
                )
            else:
                session._pending_prompt = user_message
                session.add_message("user", user_message)
                prompt = session._build_prompt(user_message)

        if self._gen.weights is None:
            yield _sse({"type": "error", "text": "Model not loaded", "done": True})
            with session._lock:
                session.state = SessionState.ERROR
            return

        generated_this_call = ""

        try:
            tokens = self._gen.tokenizer.encode(prompt)
            token_budget = max_tokens
            chunk_buf = ""

            while token_budget > 0:
                # Check stop flag
                if session._stop_event.is_set():
                    with session._lock:
                        session._generated_so_far += generated_this_call
                        session.state = SessionState.PAUSED
                    yield _sse(
                        {
                            "type": "paused",
                            "text": "",
                            "done": False,
                        }
                    )
                    return

                # Generate a small chunk
                chunk_size = min(CHUNK_TOKENS, token_budget)
                chunk_text = self._gen.generate(
                    self._gen.tokenizer.decode(tokens),
                    max_new_tokens=chunk_size,
                    temperature=temperature,
                    throttle_ms=0,
                    stop_sequences=["\n\n\n\n"],
                )
                # Extract only the new part
                decoded_prompt = self._gen.tokenizer.decode(tokens)
                new_text = chunk_text[len(decoded_prompt) :]

                if not new_text:
                    break

                # Append new tokens to context
                new_ids = self._gen.tokenizer.encode(new_text)
                tokens = (tokens + new_ids)[-(self._gen._max_seq) :]
                token_budget -= len(new_ids)
                generated_this_call += new_text
                chunk_buf += new_text

                # Flush chunk to SSE
                yield _sse(
                    {
                        "type": "token",
                        "text": chunk_buf,
                        "done": False,
                    }
                )
                chunk_buf = ""

                # Natural stop: model generated a strong ending
                if _looks_complete(generated_this_call):
                    break

            # Generation finished naturally
            full_response = session._generated_so_far + generated_this_call
            with session._lock:
                session._generated_so_far = ""
                session._pending_prompt = ""
                session.state = SessionState.DONE
                session.add_message("assistant", full_response)

            yield _sse({"type": "done", "text": "", "done": True})

        except Exception as exc:
            logger.exception("Chat generation error")
            _ = exc  # suppress TRY401
            with session._lock:
                session.state = SessionState.ERROR
            yield _sse(
                {
                    "type": "error",
                    "text": f"Ошибка: {exc}",
                    "done": True,
                }
            )

    def continue_stream(
        self,
        session_id: str,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = TEMPERATURE,
    ) -> Generator[str, None, None]:
        """
        Resume a PAUSED session from where it stopped.

        Yields the same SSE format as :meth:`generate_stream`.
        """
        session = self._sessions.get(session_id)
        if session is None:
            yield _sse({"type": "error", "text": "Session not found", "done": True})
            return

        if session.state != SessionState.PAUSED:
            yield _sse(
                {
                    "type": "error",
                    "text": f"Cannot continue — session state is {session.state.value}",
                    "done": True,
                }
            )
            return

        # Clear stop flag and re-enter generate_stream
        # (it detects _generated_so_far and resumes the prompt)
        yield from self.generate_stream(
            session_id,
            user_message="",  # ignored when _generated_so_far is set
            max_tokens=max_tokens,
            temperature=temperature,
        )

    def stop_session(self, session_id: str) -> bool:
        """Signal the generator to pause.  Returns True if session found."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session._stop_event.set()
        return True


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _sse(data: dict[str, object]) -> str:
    """Format a dict as a Server-Sent Events data line."""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


def _looks_complete(text: str) -> bool:
    """
    Heuristic: True if the generated text looks self-contained.

    Triggers on common natural ending patterns so the model doesn't
    run indefinitely on open-ended prompts.
    """
    endings = [
        "\n\n---\n",
        "\n\nКонец.",
        "\n\nEnd.",
        "\n\n# End",
        "\n\nif __name__",
        "\n\n```\n\n",
        "\n\n}\n\n",
    ]
    return any(text.endswith(e) for e in endings)
