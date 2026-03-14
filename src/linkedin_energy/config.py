"""Configuration for feed sources and tagging rules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class FeedSource:
    name: str
    url: str
    tags: List[str]


# Indonesian-focused feeds (priority)
INDONESIA_FEEDS: List[FeedSource] = [
    FeedSource(
        name="ESDM - News",
        url="https://esdm.go.id/feed/",
        tags=["indonesia_first"],
    ),
    FeedSource(
        name="PLN News",
        url="https://www.pln.co.id/berita/rss.xml",
        tags=["indonesia_first"],
    ),
    FeedSource(
        name="Katadata Energy",
        url="https://katadata.co.id/rss/berita/energi",
        tags=["indonesia_first"],
    ),
    FeedSource(
        name="CNBC Indonesia Energy",
        url="https://www.cnbcindonesia.com/market/rss/energi",
        tags=["indonesia_first"],
    ),
]

# Global energy feeds
GLOBAL_FEEDS: List[FeedSource] = [
    FeedSource(
        name="IEA News",
        url="https://www.iea.org/rss/news",
        tags=["global"],
    ),
    FeedSource(
        name="BloombergNEF",
        url="https://about.bnef.com/feed/",
        tags=["global"],
    ),
    FeedSource(
        name="Reuters Energy",
        url="http://feeds.reuters.com/reuters/energy",
        tags=["global"],
    ),
    FeedSource(
        name="S&P Global Commodity Insights",
        url="https://www.spglobal.com/commodityinsights/en/rss/real-time-news",
        tags=["global"],
    ),
]

ALL_FEEDS: List[FeedSource] = INDONESIA_FEEDS + GLOBAL_FEEDS

# Storage / database settings
DB_PATH = "data/articles.db"

# Tag used for weekly journal spotlight entries
JOURNAL_SPOTLIGHT_TAG = "journal_spotlight"
