#!/usr/bin/env bash
set -e

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
  echo "Add your ANTHROPIC_API_KEY to .env before continuing."
  exit 1
fi

docker compose up -d

echo ""
echo "Services started:"
echo "  API:  http://localhost:8000/health"
echo "  n8n:  http://localhost:5678  (login: admin / changeme)"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:5678 and log in"
echo "  2. Go to Credentials and add:"
echo "     - Notion API (internal integration token)"
echo "     - LinkedIn OAuth2"
echo "  3. Import n8n/linkedin_energy_workflow.json"
echo "  4. Open the workflow, attach credentials to the Notion and LinkedIn nodes"
echo "  5. Toggle the workflow Active"
