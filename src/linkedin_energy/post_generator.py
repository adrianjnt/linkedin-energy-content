"""Generate LinkedIn post content from scraped articles."""

from __future__ import annotations

from typing import Dict, List, Optional

from .claude_client import ClaudeClient
from .storage import ArticleRecord


def _build_prompt(article: ArticleRecord, indonesia_first: bool = True) -> str:
    """Build a Claude prompt for creating a LinkedIn post."""
    direction = "Indonesia-first" if indonesia_first else "global-first"
    tags = ", ".join(article.tags) if article.tags else ""

    prompt = f"""
You are an expert content creator for a LinkedIn audience focused on the energy transition.
Produce a LinkedIn post in Indonesian (Bahasa Indonesia) with a mix of English technical terms where appropriate.

Context:
- Source title: {article.title}
- Source URL: {article.url}
- Summary / excerpt: {article.summary}
- Source: {article.source}
- Tags: {tags}

Style:
- Keep it punchy (4-6 short paragraphs)
- Include 2-3 relevant hashtags (e.g., #energi, #netzero, #transformasienergi)
- Suggest a call-to-action such as asking readers to comment or share.

Requirements:
- {direction} (prioritize Indonesian context first, then add optional global context).
- Include at least one sentence that references Indonesia or Indonesian energy policy/market.
- Do NOT exceed 600 words.
"""
    return prompt.strip()


def generate_linkedin_post(
    article: ArticleRecord,
    indonesia_first: bool = True,
    client: Optional[ClaudeClient] = None,
) -> str:
    if client is None:
        client = ClaudeClient()

    prompt = _build_prompt(article, indonesia_first=indonesia_first)
    return client.generate(prompt)
