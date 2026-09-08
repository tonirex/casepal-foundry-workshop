# Admin & Pre-Workshop Logistics — CasePal Foundry Workshop

> For the operator/admin and lead facilitator. Complete these steps before participants arrive. Target cohort: **20 attendees** in one shared Foundry project.

## Timeline

| When | Task |
|---|---|
| T-1 week | Confirm subscription, region, quota, attendee UPNs, and facilitator identity. |
| T-2 days | Deploy models, assign RBAC for 20 UPNs, create App Insights connection, deploy MCP server. |
| T-1 day | Ingest the CasePal knowledge pack, run one Navigator and one Builder dry-run. |
| Morning of | Check endpoint, models, RBAC, knowledge index, traces, and MCP URL. |

## Region and project

Use a shared Microsoft Foundry project named `casepal-workshop`.

- Preferred region: **Sweden Central**.
- Fallback: **East US** if quota or service availability blocks the preferred region.
- Share `FOUNDRY_PROJECT_ENDPOINT` with Builder participants.
- Use `casepal-<initials>` naming so 20 participants can coexist in one project.

## Model deployments

Pre-deploy these before the day; attendees with Foundry User cannot deploy models.

| Deployment name | Use |
|---|---|
| `model-router` | Default for all labs and portal agents. |
| `gpt-5.5` | Reasoning model for ambiguous or novel cases. |
| `gpt-5.4-mini` | Fast path for clean intake and routine prompts. |
| `text-embedding-3-small` | Knowledge indexing for `casepal-knowledge`. |

Warm each deployment with one smoke prompt after provisioning.

## RBAC for 20 attendees

Role IDs are used to avoid display-name drift.

| Identity | Role | Role ID | Purpose |
|---|---|---|---|
| Each attendee | Foundry User | `53ca6127-db72-4b80-b1b0-d745d6d5456d` | Build/run agents and use shared resources. |
| Lead facilitator | Foundry Project Manager | `eadc314b-1a2d-4efa-be10-5d325db5065e` | Publish the Lab 5 hosted-agent demo. |

PowerShell:

```powershell
az login
.ssign-foundry-rbac.ps1 -ResourceId "<foundry-resource-id>" -AttendeesFile attendees.txt -Facilitator facilitator@example.test
```

Bash:

```bash
az login
./assign-foundry-rbac.sh "<foundry-resource-id>" attendees.txt facilitator@example.test
```

Create `attendees.txt` from `attendees.example.txt` and include 20 UPNs or object IDs. Verify one attendee:

```bash
az role assignment list --assignee user01@example.test --scope <foundry-resource-id> -o table
```

## App Insights and tracing

Create the Application Insights resource and connect it to the Foundry project before Lab 3. Participants can still run chat without it, but the full Traces tab and evaluator history are strongest with this connection in place. Confirm a guarded prompt produces a trace before the session starts.

## Knowledge pack ingestion

Use the synthetic CasePal artefacts:

- `content/assets/case-packages.jsonl` — 15 dossier bundles used by Builder scripts.
- `content/knowledge/sop-library/` — SOPs for completeness, classification, clinical evaluation, prior cases, and RFI drafting.
- `content/knowledge/prior-cases/` — institutional memory.
- `content/knowledge/references/` — reference explainers.
- `content/knowledge/fake-registry.md` — synthetic names registry.

Upload `content/knowledge/**` to the grounding container and create/refresh a Foundry IQ index named `casepal-knowledge` using `text-embedding-3-small`. Smoke test: query `CardioFlow` and confirm `case-A2024-042` is in the top results.

## MCP mock case-management server

Deploy the Lab 5 server from `content/assets/mcp-case-management/` to Azure Container Apps:

```powershell
cd contentssets\mcp-case-management
.\deploy-mcp.ps1 -Location swedencentral
```

or:

```bash
cd content/assets/mcp-case-management
./deploy-mcp.sh
```

Share the printed `/mcp` URL. In Foundry, configure read tools as no-approval and write tools (`create_case`, `update_case_status`) as approval-required.

## Publish limitation

Participants receive Foundry User. That role cannot Publish hosted agents. Lab 5 Part B is therefore **facilitator-demo-only** and must be run by the facilitator identity with Foundry Project Manager.

## Dry-run checklist

- [ ] `casepal-reference` agent exists and can answer Lab 0 prompts.
- [ ] `casepal-knowledge` index returns SOP and prior-case citations.
- [ ] Builder: `python content/assets/lab1_intake.py` starts and can create an agent.
- [ ] Eval dataset files parse: `casepal-eval-dataset.csv` and `.jsonl`.
- [ ] MCP `/mcp` URL is reachable and first create on a fresh store returns `CMS-2026-1188`.
- [ ] Hosted deploy demo has facilitator permissions and a tested curl command.
