"""Utilities for deduplicating articles."""

from __future__ import annotations

import hashlib


def url_hash(url: str) -> str:
    """Compute an SHA256 hash for a URL (lowercased, trimmed)."""
    normalized = url.strip().lower().encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()
