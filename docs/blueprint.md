# Blueprint: Indonesia-First Energy Content Generator

This document outlines the architecture and responsibilities of each component in this repo.

## Goals

1. **Ingest energy news** on a schedule from local Indonesian sources and global outlets.
2. **Deduplicate** by URL and tag items for `indonesia_first` vs `global`.
3. **Highlight Indonesian research** weekly using SINTA / Google Scholar.
4. **Generate LinkedIn posts** using Claude, prioritizing Indonesian context first.

## High-Level Architecture

### 1) Scraper Layer (RSS + optional HTML scraping)

- Periodically run `scripts/run_scraper.py`.
- Reads RSS feed configuration in `src/linkedin_energy/config.py`.
- Uses `feedparser` to fetch and normalize items.
- Stores the results in a local SQLite database (`data/articles.db`).

### 2) Storage Layer

- `src/linkedin_energy/storage.py` handles persistence.
- Stores articles with these properties:
  - `url`, `title`, `summary`, `published`, `source`, `tags`
  - `url_hash` (SHA256) for deduplication
  - `raw_payload` for later reference

### 3) Deduplication

- Each item is hashed by its normalized `url`.
- Before insertion, the store checks if the hash exists.
- This prevents repeated scraping cycles from creating duplicates.

### 4) Journal Spotlight (Weekly)

- `scripts/weekly_spotlight.py` runs once a week.
- Uses `src/linkedin_energy/journal_spotlight.py` to query the web (via `scholarly`, etc.) for Indonesian-affiliated energy researchers.
- Stores the spotlight as an article tagged `journal_spotlight` and `indonesia_first`.

### 5) Post Generation (Claude)

- `src/linkedin_energy/claude_client.py` wraps the Anthropic Claude API.
- `src/linkedin_energy/post_generator.py` contains a prompt template:
  - Indonesian market/context first
  - Expand with global energy trends
  - Add hashtags and CTA for engagement

## Recommended Workflow

1. Run scraper daily (or multiple times per day) using a scheduler.
2. Sometime during the week, run the weekly journal spotlight script.
3. Use the post generator to craft LinkedIn content from selected articles.

## Scalability Notes

- For scale you can replace SQLite with Postgres or a managed database.
- Add a small web UI or a Slack/Telegram bot to choose which article to post.
- Add a LinkedIn publishing integration using LinkedIn API.
