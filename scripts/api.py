"""FastAPI wrapper around the LinkedIn energy pipeline for n8n integration."""

from __future__ import annotations

import logging
from typing import Annotated

from fastapi import FastAPI, Query

from linkedin_energy.config import DB_PATH
from linkedin_energy.post_generator import generate_linkedin_post
from linkedin_energy.rss_scraper import scrape_feeds
from linkedin_energy.storage import list_articles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="LinkedIn Energy API")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/scrape")
def scrape() -> dict:
    results = scrape_feeds(DB_PATH)
    logger.info("Scrape complete: %s", results)
    return results


@app.post("/generate")
def generate(indonesia_first: Annotated[bool, Query()] = True) -> dict:
    articles = list_articles(DB_PATH, limit=1)
    if not articles:
        return {"error": "No articles found. Run /scrape first."}
    article = articles[0]
    post = generate_linkedin_post(article, indonesia_first=indonesia_first)
    return {
        "post": post,
        "article_title": article.title,
        "article_url": article.url,
        "source": article.source,
        "tags": article.tags,
    }
