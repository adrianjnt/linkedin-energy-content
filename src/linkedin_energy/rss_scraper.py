"""Scrape RSS feeds and normalize items into the storage layer."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

import feedparser

from .config import ALL_FEEDS
from .storage import ArticleRecord, init_db, insert_article

logger = logging.getLogger(__name__)


def _normalize_entry(entry: Dict[str, Any], source_name: str, tags: List[str]) -> ArticleRecord:
    # Some feeds use summary, some use description.
    summary = entry.get("summary") or entry.get("description") or ""
    title = entry.get("title") or "(no title)"
    link = entry.get("link") or entry.get("id") or ""

    published = None
    if entry.get("published"):
        published = entry.get("published")
    elif entry.get("updated"):
        published = entry.get("updated")

    return ArticleRecord(
        url=link,
        title=title,
        summary=summary,
        published=published,
        source=source_name,
        tags=tags,
        raw_payload=entry,
    )


def scrape_feeds(db_path: str, feeds: Optional[Iterable] = None) -> Dict[str, int]:
    """Scrape configured RSS feeds and write new items to the DB."""
    init_db(db_path)
    results: Dict[str, int] = {"inserted": 0, "skipped": 0}

    if feeds is None:
        feeds = ALL_FEEDS

    for feed in feeds:
        logger.info("Fetching %s (%s)", feed.name, feed.url)
        parsed = feedparser.parse(feed.url)
        if parsed.bozo:
            logger.warning("Failed to parse feed %s: %s", feed.url, parsed.bozo_exception)

        for entry in parsed.entries:
            article = _normalize_entry(entry, source_name=feed.name, tags=feed.tags)
            inserted = insert_article(db_path, article)
            if inserted:
                results["inserted"] += 1
            else:
                results["skipped"] += 1

    return results


def latest(db_path: str, limit: int = 10):
    """Convenience helper to fetch the latest articles."""
    from .storage import list_articles

    return list_articles(db_path, limit=limit)
