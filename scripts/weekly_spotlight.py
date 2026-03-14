"""Weekly journal spotlight (Indonesian authors in energy)."""

from __future__ import annotations

import logging

from linkedin_energy.config import DB_PATH
from linkedin_energy.journal_spotlight import find_indonesian_energy_research
from linkedin_energy.storage import insert_article

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def main() -> None:
    spotlight = find_indonesian_energy_research()
    if not spotlight:
        logging.warning("No spotlight article found. Adjust search parameters or proxy settings.")
        return

    inserted = insert_article(DB_PATH, spotlight)
    if inserted:
        logging.info("Inserted journal spotlight: %s", spotlight.title)
    else:
        logging.info("Journal spotlight already exists in the database.")


if __name__ == "__main__":
    main()
