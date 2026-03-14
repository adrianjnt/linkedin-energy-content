# Deployment & Automation Guide

## Local Scheduling (Development)

### Windows Task Scheduler

To run the scraper daily on Windows:

1. Open **Task Scheduler** (`taskschd.msc`)
2. Create Basic Task:
   - **Name:** `LinkedIn Energy Scraper`
   - **Trigger:** Daily at 8:00 AM
   - **Action:** Run a program
   - **Program:** `C:\Users\PLN\AppData\Local\Programs\Python\Python313\python.exe`
   - **Add arguments:** `-u scripts/run_scraper.py --db data/articles.db`
   - **Start in:** `D:\OneDrive - PLN\LinkedIn`

### Weekly Spotlight (Friday)

1. Create another task:
   - **Name:** `LinkedIn Energy Journal Spotlight`
   - **Trigger:** Weekly on Friday at 2:00 PM
   - **Action:** Run program (same as above)
   - **Add arguments:** `-u scripts/weekly_spotlight.py`

## Cloud Deployment

### Option 1: Google Cloud Scheduler + Cloud Run

```bash
# Build Docker image
docker build -t linkedin-energy-scraper .

# Push to Google Cloud Registry
docker tag linkedin-energy-scraper gcr.io/YOUR_PROJECT/linkedin-energy-scraper
docker push gcr.io/YOUR_PROJECT/linkedin-energy-scraper

# Deploy to Cloud Run
gcloud run deploy linkedin-energy-scraper \
  --image gcr.io/YOUR_PROJECT/linkedin-energy-scraper \
  --region us-central1
```

Then set up Cloud Scheduler to trigger the endpoint daily.

### Option 2: AWS Lambda

1. Package the app as a Lambda deployment
2. Set up EventBridge (CloudWatch Events) to trigger daily

### Option 3: GitHub Actions

Add `.github/workflows/scrape.yml`:

```yaml
name: Scrape Energy News

on:
  schedule:
    - cron: '0 8 * * *'  # Daily at 8 AM UTC

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: PYTHONPATH=src python scripts/run_scraper.py
      - uses: actions/upload-artifact@v3
        with:
          name: articles-db
          path: data/articles.db
```

## Publishing to LinkedIn

### Option 1: Manual

After running `python scripts/generate_post.py --latest`, copy the output and post manually on LinkedIn.

### Option 2: LinkedIn API (OAuth)

Integrate the LinkedIn Share API:

```python
# In post_generator.py, add:
import requests

def publish_to_linkedin(post_text, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "commentary": post_text,
        "visibility": "PUBLIC"
    }
    response = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        json=payload,
        headers=headers
    )
    return response.json()
```

### Option 3: LinkedIn API Integration Service

Use a service like **Buffer**, **Later**, or **Hootsuite** that provides APIs for scheduling posts.

## Database Backup

For production, back up `data/articles.db` to cloud storage:

```powershell
# Weekly backup to OneDrive (already in your path!)
Copy-Item data/articles.db "d:\OneDrive - PLN\LinkedIn\backups\articles_$(Get-Date -Format 'yyyyMMdd').db"
```

Or upload to S3/GCS:

```bash
aws s3 cp data/articles.db s3://your-bucket/backups/articles_$(date +%Y%m%d).db
```

## Monitoring

Add logging to track scraper runs:

```python
# In scripts/run_scraper.py
import logging

logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

View logs:
```powershell
tail -f logs/scraper.log
```
