#!/usr/bin/env bash
# CasePal workshop — one-time setup for the 🔵 Builder rails.
# Safe to re-run. Works in Codespaces and any bash shell (macOS/Linux/WSL).
set -euo pipefail

cd "$(dirname "$0")"   # content/assets

echo "==> CasePal workshop setup"

# 1) Dependencies (already installed in Codespaces via devcontainer; harmless to re-run).
if [ -f requirements.txt ]; then
  echo "==> Installing Python dependencies..."
  python -m pip install --quiet --upgrade pip
  pip install --quiet -r requirements.txt
fi

# 2) Azure sign-in (needed by DefaultAzureCredential).
if az account show >/dev/null 2>&1; then
  echo "==> Already signed in to Azure as: $(az account show --query user.name -o tsv)"
else
  echo "==> Signing in to Azure (use your WORKSHOP account)..."
  az login --use-device-code
fi

# 3) Local .env from the template.
if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created content/assets/.env from template."
fi

cat <<'NEXT'

==> Almost done. Edit content/assets/.env and set:
      FOUNDRY_PROJECT_ENDPOINT = (ask your facilitator)
      INITIALS                 = your initials (your agents get named casepal-<initials>)

    Then run a lab:
      python lab1_intake.py            # 🔵 Builder script
      # or open lab1_intake.ipynb and Run All   # 🔵 Builder notebook
NEXT
