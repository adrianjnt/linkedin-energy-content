#!/bin/bash
set -e

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example"
  echo ">> Edit .env and add your ANTHROPIC_API_KEY, then re-run this script."
  exit 1
fi

if grep -q "sk-your-key-here" .env; then
  echo ">> ERROR: Replace ANTHROPIC_API_KEY in .env before starting."
  exit 1
fi

mkdir -p data logs

docker compose up -d --build

echo ""
echo "Done! Services running:"
echo "  API:  http://localhost:8000/docs"
echo "  n8n:  http://localhost:5678"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:5678 and log in (admin / changeme)"
echo "  2. Go to Credentials -> New -> LinkedIn OAuth2 and connect your account"
echo "  3. Import n8n/linkedin_energy_workflow.json via Workflows -> Import"
echo "  4. Open the workflow, attach your LinkedIn credential, and toggle it Active"
echo ""
echo "The workflow will then post automatically Mon-Fri at 9am."
echo "To test immediately: open the workflow and click 'Execute Workflow'."
