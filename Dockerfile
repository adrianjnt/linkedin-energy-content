FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ src/
COPY scripts/ scripts/
COPY .env.example .env

# Create data directory for SQLite
RUN mkdir -p data

# Default command: run the scraper
CMD ["python", "-m", "linkedin_energy.rss_scraper"]
