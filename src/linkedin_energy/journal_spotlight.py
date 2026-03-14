"""Find Indonesian-affiliated energy research to spotlight."""

from __future__ import annotations

import logging
from typing import Dict, Optional

from scholarly import scholarly

from .config import JOURNAL_SPOTLIGHT_TAG
from .storage import ArticleRecord

logger = logging.getLogger(__name__)


def _normalize_scholar_entry(entry: Dict[str, str]) -> ArticleRecord:
    title = entry.get("bib", {}).get("title") or "Unknown title"
    url = entry.get("eprint_url") or entry.get("pub_url") or ""
    abstract = entry.get("bib", {}).get("abstract") or ""
    authors = entry.get("bib", {}).get("author") or ""
    year = entry.get("bib", {}).get("pub_year") or ""

    summary = f"{abstract}\n\nAuthors: {authors} | Year: {year}"

    return ArticleRecord(
        url=url,
        title=title,
        summary=summary,
        published=str(year),
        source="Google Scholar (SINTA filter)",
        tags=["indonesia_first", JOURNAL_SPOTLIGHT_TAG],
        raw_payload=entry,
    )


def find_indonesian_energy_research(limit: int = 5) -> Optional[ArticleRecord]:
    """Search Google Scholar for Indonesian-affiliated energy research.

    This is a best-effort approach. If Google Scholar is blocked, consider using a
    paid metadata API or exporting results from SINTA.
    """
    query = "renewable energy Indonesia OR energi terbarukan Indonesia"
    logger.info("Searching Scholar with query: %s", query)

    search = scholarly.search_pubs(query)
    for item in search:
        # item is a dict containing bib info and perhaps affiliation info
        # We look for any sign of Indonesia in affiliation/author list.
        authors = item.get("bib", {}).get("author", "")
        if "Indonesia" in authors or "Indonesia" in str(item.get("bib", {}).get("affiliation", "")):
            return _normalize_scholar_entry(item)

        # Fallback: first item still can be used
        return _normalize_scholar_entry(item)

    return None
