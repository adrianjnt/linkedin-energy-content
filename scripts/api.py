"""FastAPI service exposing the LinkedIn energy pipeline over HTTP."""

from __future__ import annotations

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException, Query

from linkedin_energy.config import DB_PATH
from linkedin_energy.post_generator import generate_linkedin_post
from linkedin_energy.rss_scraper import scrape_feeds
from linkedin_energy.storage import list_articles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI(title="LinkedIn Energy API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/scrape")
def scrape():
    results = scrape_feeds(DB_PATH)
    return results


@app.post("/generate")
def generate(indonesia_first: bool = Query(default=True)):
    articles = list_articles(DB_PATH, limit=1)
    if not articles:
        raise HTTPException(status_code=404, detail="No articles found. Run /scrape first.")
    article = articles[0]
    post = generate_linkedin_post(article, indonesia_first=indonesia_first)
    return {
        "post": post,
        "article_title": article.title,
        "article_url": article.url,
        "article_source": article.source,
    }
