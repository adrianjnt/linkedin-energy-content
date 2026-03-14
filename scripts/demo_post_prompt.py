"""Demo: Show how post generation works (without calling Claude API)."""

from __future__ import annotations

import sys

sys.path.insert(0, "src")

from linkedin_energy.config import DB_PATH
from linkedin_energy.post_generator import _build_prompt
from linkedin_energy.storage import list_articles

# Get the latest article
articles = list_articles(DB_PATH, limit=1)
if not articles:
    print("No articles found. Run the scraper first.")
    sys.exit(1)

article = articles[0]
print("=" * 70)
print(f"ARTICLE: {article.title}")
print(f"SOURCE: {article.source}")
print(f"TAGS: {', '.join(article.tags)}")
print("=" * 70)
print("\nPROMPT sent to Claude API:")
print("-" * 70)
prompt = _build_prompt(article, indonesia_first=True)
print(prompt)
print("-" * 70)
print("\n📝 To generate an actual post, add ANTHROPIC_API_KEY to .env and run:")
print("  python scripts/generate_post.py --latest")
