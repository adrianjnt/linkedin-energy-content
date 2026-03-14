"""Wrapper for Anthropic Claude API."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:
    import anthropic
except ImportError:  # pragma: no cover
    anthropic = None  # type: ignore[assignment]


@dataclass
class ClaudeClientConfig:
    api_key: str
    model: str = "claude-2.1"  # Change as needed
    max_tokens: int = 1000
    temperature: float = 0.7


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

        self._client = anthropic.Client(api_key=config.api_key)
        self.config = config

    def generate(self, prompt: str) -> str:
        """Generate text using Claude."""
        response = self._client.completions.create(
            model=self.config.model,
            prompt=prompt,
            max_tokens_to_sample=self.config.max_tokens,
            temperature=self.config.temperature,
        )
        return response.completion
