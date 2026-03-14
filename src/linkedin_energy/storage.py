"""Simple storage layer using SQLite for scraped articles."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .dedupe import url_hash


@dataclass
class ArticleRecord:
    url: str
    title: str
    summary: str
    published: Optional[str]
    source: str
    tags: List[str] = field(default_factory=list)
    url_hash: str = ""
    raw_payload: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def __post_init__(self):
        if not self.url_hash:
            self.url_hash = url_hash(self.url)


def _get_conn(path: str) -> sqlite3.Connection:
    db_file = Path(path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_file), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str) -> None:
    """Initialize the SQLite database schema."""
    with _get_conn(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                url_hash TEXT NOT NULL UNIQUE,
                title TEXT,
                summary TEXT,
                published TEXT,
                source TEXT,
                tags TEXT,
                raw_payload TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()


def insert_article(db_path: str, article: ArticleRecord) -> bool:
    """Insert an article if it is not already present.

    Returns True if inserted, False if duplicate.
    """
    article = ArticleRecord(**asdict(article))

    with _get_conn(db_path) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO articles (url, url_hash, title, summary, published, source, tags, raw_payload, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    article.url,
                    article.url_hash,
                    article.title,
                    article.summary,
                    article.published,
                    article.source,
                    json.dumps(article.tags, ensure_ascii=False),
                    json.dumps(article.raw_payload, ensure_ascii=False),
                    article.created_at,
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def list_articles(
    db_path: str,
    limit: int = 20,
    tags: Optional[Iterable[str]] = None,
    order_desc: bool = True,
) -> List[ArticleRecord]:
    """Return a list of articles (newest first by default)."""
    with _get_conn(db_path) as conn:
        sql = "SELECT * FROM articles"
        params: List[Any] = []
        if tags:
            # Simple tag filtering; this is not optimized for huge datasets.
            tag_clauses = " OR ".join(["tags LIKE ?" for _ in tags])
            sql += f" WHERE ({tag_clauses})"
            params = [f"%{t}%" for t in tags]
        sql += " ORDER BY created_at " + ("DESC" if order_desc else "ASC")
        sql += " LIMIT ?"
        params.append(limit)

        rows = conn.execute(sql, params).fetchall()

    results: List[ArticleRecord] = []
    for row in rows:
        results.append(
            ArticleRecord(
                url=row["url"],
                title=row["title"],
                summary=row["summary"],
                published=row["published"],
                source=row["source"],
                tags=json.loads(row["tags"] or "[]"),
                url_hash=row["url_hash"],
                raw_payload=json.loads(row["raw_payload"] or "{}"),
                created_at=row["created_at"],
            )
        )
    return results


def find_article_by_hash(db_path: str, url_hash_value: str) -> Optional[ArticleRecord]:
    with _get_conn(db_path) as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE url_hash = ? LIMIT 1", (url_hash_value,)
        ).fetchone()
        if not row:
            return None
        return ArticleRecord(
            url=row["url"],
            title=row["title"],
            summary=row["summary"],
            published=row["published"],
            source=row["source"],
            tags=json.loads(row["tags"] or "[]"),
            url_hash=row["url_hash"],
            raw_payload=json.loads(row["raw_payload"] or "{}"),
            created_at=row["created_at"],
        )
