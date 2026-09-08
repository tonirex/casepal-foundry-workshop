# Hosted CasePal — Lab 5 Part B facilitator demo

This scaffold exposes a small `/chat` API that forwards messages to a CasePal Foundry Agent. It is used after the MCP case-management demo to show that the same agent can be hosted behind an application endpoint.

> Participants with Foundry User cannot publish hosted agents. Run this demo with the facilitator identity that has Foundry Project Manager.

## Local sanity check

```powershell
copy .env.example .env
pip install -r src/requirements.txt
az login
python src/agent.py
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d "{"messages":[{"role":"user","content":"Hi"}]}"
```

## Deploy

Use the VS Code Microsoft Foundry toolkit or `azd up` from this folder. The service reads:

- `FOUNDRY_PROJECT_ENDPOINT`
- `FOUNDRY_MODEL_NAME` (default `model-router`)
- `AGENT_NAME` (default `casepal-hosted`)

## Lab 5 demo prompt

Send the canonical MCP prompt for `MDR-2026-0135`. The hosted service should call the Foundry agent; the agent's MCP tool configuration in Foundry handles approval-before-write and returns a `CMS-2026-<n>` case ID.
