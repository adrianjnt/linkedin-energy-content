"""Run the RSS scraper and store results."""

from __future__ import annotations

import argparse
import logging

from linkedin_energy.config import DB_PATH
from linkedin_energy.rss_scraper import scrape_feeds

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the RSS feed scraper.")
    parser.add_argument(
        "--db", default=DB_PATH, help="Path to the SQLite DB (default: data/articles.db)"
    )
    args = parser.parse_args()

    results = scrape_feeds(args.db)
    logging.info("Scraper finished. inserted=%s skipped=%s", results["inserted"], results["skipped"])


if __name__ == "__main__":
    main()
