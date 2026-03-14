"""Generate a LinkedIn post from the latest scraped article."""

from __future__ import annotations

import argparse
import logging

from linkedin_energy.config import DB_PATH
from linkedin_energy.post_generator import generate_linkedin_post
from linkedin_energy.storage import list_articles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate LinkedIn post text from a scraped article.")
    parser.add_argument(
        "--db", default=DB_PATH, help="Path to the SQLite DB (default: data/articles.db)"
    )
    parser.add_argument(
        "--latest", action="store_true", help="Generate a post for the latest article."
    )
    parser.add_argument(
        "--indonesia-first",
        action="store_true",
        help="Prioritize an Indonesia-first angle in the generated post (default).",
    )
    parser.add_argument(
        "--global-first",
        action="store_true",
        help="Prioritize global context in the generated post.",
    )

    args = parser.parse_args()

    if not args.latest:
        parser.error("Please specify --latest (future enhancements may support selecting by URL/ID).")

    articles = list_articles(args.db, limit=1)
    if not articles:
        logging.error("No articles found. Run the scraper first.")
        return

    article = articles[0]
    indonesia_first = True
    if args.global_first:
        indonesia_first = False

    post = generate_linkedin_post(article, indonesia_first=indonesia_first)
    print(post)


if __name__ == "__main__":
    main()
