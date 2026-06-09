"""Wrapper for Anthropic Claude API."""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import Optional

try:
    import anthropic
except ImportError:  # pragma: no cover
    anthropic = None  # type: ignore[assignment]

from .config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CLAUDE_TEMPERATURE

logger = logging.getLogger(__name__)


@dataclass
class ClaudeClientConfig:
    api_key: str
    model: str = CLAUDE_MODEL
    max_tokens: int = CLAUDE_MAX_TOKENS
    temperature: float = CLAUDE_TEMPERATURE


class ClaudeClient:
    def __init__(self, config: Optional[ClaudeClientConfig] = None):
        if anthropic is None:
            raise RuntimeError(
                "Missing dependency: install `anthropic`. See requirements.txt."
            )

        if config is None:
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise RuntimeError("ANTHROPIC_API_KEY is not set in the environment")
            config = ClaudeClientConfig(api_key=api_key)

        self._client = anthropic.Anthropic(api_key=config.api_key)
        self.config = config

    def generate(self, prompt: str) -> str:
        """Generate text using Claude."""
        logger.debug("Sending prompt to Claude model %s", self.config.model)
        response = self._client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
