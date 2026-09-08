# CasePal — workshop starter assets

Runnable reference code for the 🔵 **Builder** rail. The 🟢 Navigator rail is portal-only.

## Layout

```
assets/
  common/casepal_common.py        # shared Foundry helpers and canonical instructions
  lab1_intake.py/.ipynb           # structured intake and model-router checks
  lab2_rag.py/.ipynb              # knowledge retrieval and institutional memory
  lab3_eval.py/.ipynb             # guardrails, evaluators, trace-ready dataset
  lab4_multiagent.py/.ipynb       # orchestrator + four specialists
  lab4_multiagent_concurrent.py   # concurrent specialist variant
  mcp-case-management/            # Lab 5 mock Case Management System MCP server
  hosted-deploy/                  # Lab 5 hosted-agent facilitator demo
  case-packages.jsonl             # 15 synthetic dossiers
  casepal-eval-dataset.csv/jsonl  # Lab 3 evaluation rows
```

## Setup

```bash
pip install -r requirements.txt
az login --use-device-code
cp .env.example .env
# edit FOUNDRY_PROJECT_ENDPOINT and INITIALS
```

Windows PowerShell:

```powershell
python -m venv .venv ; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
az login
copy .env.example .env
$env:PYTHONIOENCODING = "utf-8"
```

## Run

```powershell
python lab1_intake.py
python lab2_rag.py
python lab3_eval.py
python lab4_multiagent.py
```

All scripts use `FOUNDRY_PROJECT_ENDPOINT`, `FOUNDRY_MODEL_NAME` (default `model-router`), and `INITIALS`. The notebooks are the canonical Builder artefacts; scripts mirror the same source for facilitators who prefer terminals.
