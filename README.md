# LinkedIn Energy Content Generator (Indonesia-first)

This project scrapes energy news, builds a small content store, and generates LinkedIn posts using Anthropic Claude (via API). It is optimized for **Indonesia-first** coverage (local news + weekly Indonesian journal spotlight) and also includes global energy updates.

## Key Features

- ✅ RSS scraper for Indonesian energy news (ESDM, PLN, Katadata, CNBC Indonesia)
- ✅ Global media RSS scraping (IEA, BloombergNEF, Reuters, S&P Global Commodity Insights)
- ✅ Deduplicates articles by URL hash
- ✅ Tags each item with `indonesia_first` or `global`
- ✅ Weekly journal spotlight using SINTA/Google Scholar for Indonesian-affiliated researchers
- ✅ LinkedIn post generation with Claude via `ANTHROPIC_API_KEY`

## Getting Started

### 1) Clone / initialize repo

```powershell
cd "D:\OneDrive - PLN\LinkedIn"
# If you haven't already:
git init
```

### 2) Create Python environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3) Configure credentials

Create a `.env` file in the repo root (not checked in):

```text
ANTHROPIC_API_KEY=sk-...
```

Or copy `.env.example` and fill in your API key:
```powershell
copy .env.example .env
```

### 4) Run the scraper

```powershell
# Scrape latest RSS articles and store into db
python scripts/run_scraper.py
```

### 5) Generate a LinkedIn post for the latest article

```powershell
python scripts/generate_post.py --latest
```

### 6) See a demo of the prompt sent to Claude

```powershell
python scripts/demo_post_prompt.py
```

### 7) Run weekly journal spotlight

```powershell
python scripts/weekly_spotlight.py
```

## Push to GitHub

1. Create a new repo on GitHub (e.g., `linkedin-energy-content`)
2. Add the remote and push:

```powershell
git remote add origin https://github.com/YOUR_USERNAME/linkedin-energy-content.git
git branch -M main
git push -u origin main
```

## Project Layout

- `src/linkedin_energy/` – core scraper, storage, and generator code
- `scripts/` – CLI wrappers for common workflows
- `docs/blueprint.md` – architecture & blueprint for how the system works

## Notes

- This repo is a starting point: you can swap scrape targets, build a web dashboard, or automate publishing via LinkedIn API.
- For production scheduling, use **cron** (Linux) or **Cloud Scheduler** (GCP/AWS) to call scripts regularly.
