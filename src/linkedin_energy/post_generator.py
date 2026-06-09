"""Generate LinkedIn post content from scraped articles."""

from __future__ import annotations

import logging
from typing import Optional

from .claude_client import ClaudeClient
from .storage import ArticleRecord

logger = logging.getLogger(__name__)

MAX_POST_WORDS = 600


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
    logger.info("Generating LinkedIn post for article: %s", article.title)
    post = client.generate(prompt)

    word_count = len(post.split())
    if word_count > MAX_POST_WORDS:
        logger.warning(
            "Generated post exceeds %d words (got %d words). Consider shortening the output.",
            MAX_POST_WORDS,
            word_count,
        )
    else:
        logger.info("Generated post word count: %d", word_count)

    return post
