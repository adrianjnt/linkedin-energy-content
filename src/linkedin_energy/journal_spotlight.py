"""Find Indonesian-affiliated energy research to spotlight."""

from __future__ import annotations

import logging
from typing import Dict, Optional

from .config import JOURNAL_SPOTLIGHT_TAG
from .storage import ArticleRecord

logger = logging.getLogger(__name__)


def _normalize_spotlight_entry(entry: Dict[str, str]) -> ArticleRecord:
    title = entry.get("title", "Unknown title")
    url = entry.get("url", "")
    abstract = entry.get("abstract", "")
    authors = entry.get("authors", "")
    year = entry.get("year", "")

    summary = f"{abstract}\n\nAuthors: {authors} | Year: {year}"

    return ArticleRecord(
        url=url,
        title=title,
        summary=summary,
        published=str(year),
        source="Energy Research (Indonesian Authors)",
        tags=["indonesia_first", JOURNAL_SPOTLIGHT_TAG],
        raw_payload=entry,
    )


def find_indonesian_energy_research(limit: int = 5) -> Optional[ArticleRecord]:
    """Search for Indonesian-affiliated energy research.

    NOT YET IMPLEMENTED. This function currently always returns None.

    To implement, integrate with one of:
      - SINTA API (https://api.sinta.ristekbrin.go.id/)
      - Google Scholar via SerpAPI or similar
      - ResearchGate or Academia.edu APIs

    Raises:
        NotImplementedError: Always, until an integration is added.
    """
    raise NotImplementedError(
        "find_indonesian_energy_research() is not yet implemented. "
        "Integrate with SINTA API or another academic-search provider and remove this error."
    )
