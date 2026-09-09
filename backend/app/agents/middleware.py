"""LangChain Agent middleware used by the trip planner."""

from __future__ import annotations

import logging
import time
from typing import Any

from langchain.agents.middleware import AgentMiddleware

logger = logging.getLogger(__name__)


class PlannerMiddleware(AgentMiddleware):
    """Protect and observe planner model calls without owning business retries."""

    def __init__(self, max_prompt_chars: int = 50000) -> None:
        self.max_prompt_chars = max_prompt_chars
        self._started_at: dict[int, float] = {}

    @property
    def name(self) -> str:
        return "planner-governance"

    def before_model(self, state: dict[str, Any], runtime: Any) -> dict[str, Any] | None:
        messages = state.get("messages", [])
        total_chars = sum(len(self._message_text(message)) for message in messages)
        if total_chars > self.max_prompt_chars:
            raise ValueError(
                f"planner prompt exceeds limit ({total_chars}>{self.max_prompt_chars} characters)"
            )
        self._started_at[id(state)] = time.perf_counter()
        logger.info("planner model call started messages=%d chars=%d", len(messages), total_chars)
        return None

    def after_model(self, state: dict[str, Any], runtime: Any) -> dict[str, Any] | None:
        started_at = self._started_at.pop(id(state), None)
        elapsed_ms = (time.perf_counter() - started_at) * 1000 if started_at else 0
        messages = state.get("messages", [])
        response_chars = len(self._message_text(messages[-1])) if messages else 0
        logger.info(
            "planner model call completed elapsed_ms=%.0f response_chars=%d messages=%d",
            elapsed_ms,
            response_chars,
            len(messages),
        )
        return None

    @staticmethod
    def _message_text(message: Any) -> str:
        content = getattr(message, "content", None)
        if content is None and isinstance(message, dict):
            content = message.get("content", "")
        if isinstance(content, list):
            return " ".join(str(item.get("text", item)) if isinstance(item, dict) else str(item) for item in content)
        return str(content or "")


def build_planner_middleware() -> list[PlannerMiddleware]:
    """Build a fresh middleware list for each Agent graph."""
    return [PlannerMiddleware()]
