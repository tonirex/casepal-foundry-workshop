# CasePal Case Management — MCP server (Lab 5, Part A)

This folder contains the synthetic Case Management System used in Lab 5. CasePal connects to it as an MCP tool, and Foundry is configured to require reviewer approval before any write.

## Tools

| Tool | Purpose |
|---|---|
| `create_case(report_id, priority, follow_up_owner)` | Creates a case and returns `{ "case_id": "CMS-2026-<n>", "created_at": <iso> }`. First case is `CMS-2026-1188`. |
| `get_case(case_id)` | Reads one case by ID. |
| `update_case_status(case_id, status, note)` | Transitions `open`, `awaiting_info`, `escalated`, or `closed`. |
| `list_open_cases(owner)` | Lists open cases assigned to one owner. |

By default, cases are kept in memory. Set `MCP_PERSIST_PATH=/data/casepal.db` to use SQLite.

## Deploy once for the room

```powershell
az login
.\deploy-mcp.ps1
```

Or with bash:

```bash
az login
./deploy-mcp.sh
```

Both scripts deploy this folder to Azure Container Apps and print a public `/mcp` URL. The server is no-auth for the workshop; use a real identity boundary in production.

## Run locally

```powershell
pip install -r requirements.txt
python server.py
```

The server listens on `http://0.0.0.0:8000/mcp`.

## Map to Lab 5

1. Add the printed `/mcp` URL to the CasePal agent in Foundry.
2. Leave read tools auto-approved.
3. Require approval for `create_case` and `update_case_status` to demonstrate Pattern #6 Human-in-the-Loop Review.
4. Send the Lab 5 prompt for `MDR-2026-0135`; after approval, `create_case` returns `CMS-2026-1188` on a fresh store.
