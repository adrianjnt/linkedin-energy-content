"""Find Indonesian-affiliated energy research to spotlight."""

from __future__ import annotations

import logging
from typing import Dict, Optional

import requests

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
    
    This is a simplified version that looks up manual sources or API endpoints.
    For production, integrate with SINTA API (https://sinta.ristekbrin.go.id)
    or use Google Scholar API via a paid service.
    
    Currently returns None — you can add a manual list of known papers below.
    """
    logger.info("Searching for Indonesian energy research...")
    
    # TODO: Add integration with:
    # 1. SINTA API (https://api.sinta.ristekbrin.go.id/)
    # 2. Google Scholar via SerpAPI or similar
    # 3. ResearchGate or Academia.edu APIs
    
    # For now, return None to indicate no automatic search is available
    return None

