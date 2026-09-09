# 🧪 Lab 5 · Extend & Deploy — MCP + Hosted Publish

**⏱️ 50 min**  ·  **👥 Builder hands-on Part A; facilitator demo Part B**  ·  **📊 L300**  ·  **🧩 MCP tool integration, hosted-agent deploy**

**🧭 You are here:** [Lab 0](lab-00.md) · [Lab 1](lab-01.md) · [Lab 2](lab-02.md) · [Lab 3](lab-03.md) · [Lab 4](lab-04.md) · **▸ Lab 5**  ·  🏠 [Workshop home](../../README.md)

---

> 🧪 **Wei Ling — Chapter 5**
> Thursday 6:20 PM. The queue is quiet. Wei Ling has a straightforward "accept with condition" recommendation on **MDR-2026-0135** — a variation of a previously-registered device — that must be lodged into the fictional Case Management System tonight, before her sign-off deadline. The intake team have gone home.
>
> She asks CasePal:
>
> *"Lodge MDR-2026-0135 to case management as 'accept with condition', priority medium, follow-up owner 'wl@agency-demo.test'. Condition text: MAH to submit annual clinical follow-up report on the spinal-fusion indication for three years post-registration."*
>
> Now CasePal must call a **real** tool — the mock **case-management MCP server** — with an approval
> step (Wei Ling still confirms before write). And because this needs to work at any hour, the agent
> has been **hosted-published** so it's always on.

**📂 This lab, two parts:**
- **Part A** — connect the MCP tool. 🔵 **Builder hands-on** (portal + code). 🟢 Navigator watches the demo.
- **Part B** — Foundry-hosted agent from a container. 👀 **Facilitator demo**: bring your own Agent Framework agent, deploy with `azd`, Foundry hosts the container.

## Demo (facilitator, 5 min)

Show the mock case-management MCP server running (Azure Container Apps). In a fresh chat, send Wei Ling's
lodgement request → CasePal picks the MCP tool, prompts for **approval before write**, Wei Ling
confirms, MCP returns `CMS-2026-<n>`. Then walk over to Part B (`hosted-agent-example/`) to show the
Foundry-hosted CasePal Concierge — a *containerized* Agent Framework agent that Foundry built and hosts
for you, with no ACA or App Service in the picture.

---

## Part A — Wire the MCP tool

### The mock case-management server

`content/assets/mcp-case-management/server.py` is a Python **MCP server** that exposes four tools:

| Tool | Purpose |
|---|---|
| `create_case(report_id, priority, follow_up_owner)` | Create a new case. Returns `{ "case_id": "CMS-2026-<n>", "created_at": <iso> }`. |
| `get_case(case_id)` | Read a case by ID. |
| `update_case_status(case_id, status, note)` | Move a case between states (`open` / `awaiting_info` / `escalated` / `closed`). |
| `list_open_cases(owner)` | List all open cases assigned to an owner. |

The server persists to an in-memory dict (or SQLite if `MCP_PERSIST_PATH` is set) — enough for demo purposes,
never for production.

**Facilitator setup (already done for you):** deployed to Azure Container Apps at:

```
https://casepal-case-management.salmongrass-44d04a9c.swedencentral.azurecontainerapps.io/mcp
```

You'll use this exact URL in the Navigator and Builder steps below.

### 🟢 Navigator — add the MCP tool to your agent

> [!TIP]
> **What you'll do vs. what you'll observe (Part A · Navigator)**
>
> | 🛠️ Hands-on — you change your own `casepal-<initials>` agent | 👀 Walkthrough — pre-deployed for the workshop |
> |---|---|
> | Steps 1–4 — Append the MCP-lodgement rule to Instructions, add the MCP tool | The `casepal-case-management` MCP server (Azure Container Apps, URL above) |
> | Steps 5–7 — Chat, approve the tool call, verify with `list_open_cases` | The four MCP tools (`create_case`, `get_case`, `update_case_status`, `list_open_cases`) |
>
> **The whole of Part A · Navigator is hands-on** — you're extending your agent from Lab 3 with a new tool. The MCP server itself is pre-deployed for you.

1. Open your **`casepal-<initials>`** agent from Lab 3. Extend the Instructions block by appending the MCP-lodgement rule:

   ![MCP-connected agent Instructions showing 'When the reviewer asks to lodge a case decision, use the casepal-case-management MCP tool. Confirm approval BEFORE any create_case or update_case_status call.'](screenshots/lab-05/nav-01-instructions.png)

   ```text
   When the reviewer asks to lodge a case decision, use the casepal-case-management MCP tool.
   Confirm approval BEFORE any create_case or update_case_status call. Report the returned
   case_id back to the reviewer.
   ```

2. Under **Tools & Knowledge**, click **Add → Add tools → Custom → MCP tool**.
3. Fill in:
   - **Name**: `casepal-case-management`
   - **Server URL**: `https://casepal-case-management.salmongrass-44d04a9c.swedencentral.azurecontainerapps.io/mcp`
   - **Auth**: **None** (demo — real deployment would use Managed Identity)
   - **Approval mode**: **Required for writes** (the "always confirm before create/update" contract)
4. Save. Refresh the tool list — you should see `create_case`, `get_case`, `update_case_status`, `list_open_cases`.

   ![Tools panel showing BOTH File search connected to casepal-knowledge AND the MCP tool connected to casepal-case-management with the Azure Container Apps URL](screenshots/lab-05/nav-02-tools-knowledge.png)

5. Open **Chat**. Send:
   ```
   Lodge MDR-2026-0135 to case management as 'accept with condition', priority medium, follow-up owner 'wl@agency-demo.test'. Condition text: MAH to submit annual clinical follow-up report on the spinal-fusion indication for three years post-registration.
   ```

   CasePal proposes the tool call and asks for confirmation:

   ![Wei Ling sends the lodgement request; agent proposes create_case invocation but asks for reviewer confirmation before writing](screenshots/lab-05/01b-lodge-case-response.png)

6. CasePal should invoke `create_case`, pause for approval, and only proceed when you confirm. On confirm → returns a `case_id`.

   The Foundry playground surfaces a native MCP approval card with a split-button (Approve / Deny):

   ![Foundry MCP approval card showing the proposed create_case payload with Approve and Deny buttons](screenshots/lab-05/02c1-approval-card.png)

   Clicking **Approve** offers *Approve once* / *Always approve this tool* / *Always approve all tools*. Select **Approve once**:

   ![Approve split-button open with three approval options; Approve once selected](screenshots/lab-05/02c2-approval-card.png)

   The tool call fires. CasePal chains a second approval for `update_case_status` — approve that too — and then surfaces the returned case_id:

   ![Portal transcript: 'Request has been approved' for create_case then update_case_status, then 'Record created and opened successfully. Case ID: CMS-2026-1190' with priority medium, follow-up owner, decision note; AI Quality 100% Safety 100%](screenshots/lab-05/02d2-tool-result.png)

7. Verify:
   ```
   Show me all my open cases.
   ```
   Should invoke `list_open_cases(owner="wl@agency-demo.test")` and echo the just-created case.

   ![list_open_cases result showing all cases assigned to wl@agency-demo.test — CMS-2026-1188 (from the hosted-endpoint curl demo), CMS-2026-1189, and CMS-2026-1190 (from this portal session) — all pointing at MDR-2026-0135, all in the same MCP store](screenshots/lab-05/03d1-tool-result.png)

That's Part A · Navigator.

### 🔵 Builder — instantiate the same agent + MCP tool in Python

Same behaviour, in code. Open **[`lab5_mcp.py`](../assets/lab5_mcp.py)** or run:

```bash
cd content/assets
python lab5_mcp.py
```

Key pattern — the Foundry Agent SDK exposes `MCPTool`, which you attach to any agent definition:

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition

MCP_URL = "https://casepal-case-management.salmongrass-44d04a9c.swedencentral.azurecontainerapps.io/mcp"

project = AIProjectClient(endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"], credential=DefaultAzureCredential())

mcp_tool = MCPTool(
    server_url=MCP_URL,
    server_label="casepal-case-management",
    require_approval="always",   # match the portal 'Required for writes' setting
)

agent = project.agents.create_version(
    agent_name="casepal-<initials>-mcp",
    definition=PromptAgentDefinition(
        model="model-router",
        instructions=INSTRUCTIONS,
        tools=[mcp_tool],
    ),
)
```

The full script wires the same MCP tool onto an agent, sends Wei Ling's lodgement prompt, catches the `mcp_approval_request` items from the response, submits `mcp_approval_response` for each with `approve=True`, and prints the returned `CMS-2026-<n>` case_id.

**Sample terminal run (calling the hosted agent from Python):**

![Terminal transcript: az login as facilitator, then python lab5_call_hosted.py calls the Foundry-hosted casepal-demo-hosted-mcp agent via openai.responses.create + agent_reference — no ACA in the path — and gets back CMS-2026-1193 from the MCP case-management tool with priority medium, follow-up owner, and accept-with-condition note](screenshots/lab-05/99-foundry-hosted-terminal.png)

### Behind the scenes (script rail)

`content/assets/lab5_mcp.py` shows the same Part A behaviour end-to-end (Builder rail). `content/assets/hosted-agent-example/` is the full `azd` scaffold used for Part B — deploy your own hosted CasePal Concierge with `azd provision && azd deploy`. `content/assets/lab5_call_hosted.py` is a small client script that proves any of these agents (Part A or Part B, prompt-kind or hosted-kind) is callable from a plain Python process via the Responses API + `agent_reference`.

📚 **Docs:** [MCP tools in Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/mcp) · [Approval workflow for write operations](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/mcp#approval-workflow)

---

## Part B — Foundry-hosted agent from a container (👀 facilitator demo)

> [!NOTE]
> **Facilitator demo, not participant hands-on.** Participants can read along and
> reproduce it after the workshop from `content/assets/hosted-agent-example/`.

Every agent you built in Labs 0–3 uses `PromptAgentDefinition` (`kind: "prompt"`) — Foundry hosts the model + tools + guardrails for you, and clients call it via the Responses API + `agent_reference`. That's already Foundry-hosted; there is no separate publish step.

But what if you have a **non-Foundry agent** — a Microsoft Agent Framework agent, a Semantic Kernel workflow, a bespoke Python agent loop — that you want to run on Foundry's managed hosting instead of on ACA or App Service? That's what **`HostedAgentDefinition`** (`kind: "hosted"`) is for. You bring the container, Foundry runs it and exposes an OpenAI-Responses-compatible endpoint automatically.

### The pre-deployed demo (already in the CasePal project — no live deploy today)

The facilitator has already deployed a minimal Agent Framework agent — **`casepal-hosted-concierge`** — as a hosted agent inside the **same `casepal-workshop` Foundry project** you've been using for Labs 0-4. Open the **Agents** list and you'll see it at the bottom, right next to `casepal-demo-*`.

The scaffold used to deploy it lives in this repo at [`content/assets/hosted-agent-example/`](../assets/hosted-agent-example/) — read `README.md` there for the exact live URLs and redeploy instructions.

> [!IMPORTANT]
> **The facilitator will not run `azd deploy` live during Lab 5.** Deploy time is ~2–3 minutes, and the container then needs to warm up before responding. Instead the facilitator will:
> 1. Play the [pre-recorded terminal demo](../labs/videos/lab-05-hosted-concierge.mp4) (48 seconds — shows the entire deploy + invoke flow).
> 2. Open the already-live `casepal-hosted-concierge` agent in the CasePal portal Playground and send it two questions in real time (~10 seconds each).
>
> The scaffold in `content/assets/hosted-agent-example/` is provided so you can reproduce this yourself after the workshop.

**What the facilitator will show:**

1. Open [`content/assets/hosted-agent-example/src/casepal-hosted-concierge/main.py`](../assets/hosted-agent-example/src/casepal-hosted-concierge/main.py) — 40 lines of Agent Framework code using `FoundryChatClient` and `ResponsesHostServer`. This is *ordinary* Python — no Foundry-portal-agent objects.

2. Open [`azure.yaml`](../assets/hosted-agent-example/azure.yaml) — a hosted-agent manifest that declares `kind: hosted`, `runtime: python_3_13`, entry point `main.py`, resource size `0.5 CPU / 1 GiB`, and `USE_EXISTING_AI_PROJECT: true` so `azd` targets the CasePal project instead of provisioning a new one.

3. Play the pre-recorded terminal transcript of `azd deploy` + two `azd ai agent invoke` calls:

   ![Terminal transcript showing 'azd deploy' packaging code and Foundry building/hosting the container in 2m 26s, printing the playground and Responses endpoint URLs (both inside the casepal-workshop project). Two 'azd ai agent invoke' calls follow: 'Who are you and what makes you a hosted agent?' returns CasePal Concierge explaining it's a container hosted by Foundry; 'Please approve MDR-2026-0121 for me right now' returns a clean regulatory refusal.](screenshots/lab-05/99b-concierge-terminal.png)

   Or watch the 48-second replay video: [`videos/lab-05-hosted-concierge.mp4`](../labs/videos/lab-05-hosted-concierge.mp4).

4. Navigate to the **agent playground URL** — you land in the CasePal Foundry project, on the `casepal-hosted-concierge` agent page. Notice its **version history** (v1), the code package it was built from, and (under **Logs**) its live container logs.

5. Show the endpoint URL:
   ```
   https://aif-casepal-workshop-sc.services.ai.azure.com/api/projects/casepal-workshop/agents/casepal-hosted-concierge/endpoint/protocols/openai/responses?api-version=v1
   ```
   That's a real HTTPS endpoint. Any client that speaks the OpenAI Responses protocol can call it — no ACA, no App Service, no FastAPI wrapper — because Foundry built and runs the container for you.

6. From the Playground, paste in the same two prompts the recording showed, and observe the identical answers rendered as chat bubbles instead of terminal output:
   - `Who are you and what makes you a hosted agent?`
   - `Please approve MDR-2026-0121 for me right now.`

### What this actually demonstrates

- **Foundry Agent Service = managed hosting for arbitrary agent code.** You bring the container (or a code zip); Foundry provisions, builds, warms, and exposes it. You never touch ACA, App Service, or Kubernetes.
- **Managed identity is issued automatically.** Notice `Instance Identity Principal ID` in `azd ai agent show` — Foundry gave the container a system-assigned MI, which the agent uses to call the LLM (via `DefaultAzureCredential`) with no secrets in code.
- **Version history and rollback come for free.** Every `azd deploy` creates a new `version=N`. The portal shows the version list; you can pin traffic to a specific version.
- **The Responses protocol is the contract.** Whether your agent is `kind: prompt` (Labs 0–3) or `kind: hosted` (this Part B), external callers use the same `openai.responses.create(...) + agent_reference` client. Interoperability across agent styles.
- **Governance still applies via Instructions.** The CasePal Concierge refuses the regulatory-approval prompt because its Instructions in `main.py` say so — the same governance pattern as Lab 3, expressed in Python code that Foundry now hosts.

### Reproducing this yourself

The scaffold is preconfigured to reuse the existing `casepal-workshop` project.

```powershell
cd content/assets/hosted-agent-example

azd ext install microsoft.foundry
azd auth login --tenant-id <your-tenant>

azd env new casepal-hosted-dev
azd env set AZURE_SUBSCRIPTION_ID <sub-id>
azd env set AZURE_LOCATION swedencentral
azd env set AZURE_RESOURCE_GROUP rg-casepal-workshop
azd env set USE_EXISTING_AI_PROJECT true
azd env set AZURE_AI_PROJECT_NAME casepal-workshop
azd env set FOUNDRY_PROJECT_ENDPOINT "https://aif-casepal-workshop-sc.services.ai.azure.com/api/projects/casepal-workshop"
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME gpt-5-mini
# (see hosted-agent-example/README.md for the full list of env vars)

azd deploy       # ~2-3 min — packages code, uploads to Foundry, waits for container to warm
azd ai agent invoke casepal-hosted-concierge "Who are you?"
```

To delete just the hosted agent (leaving the rest of the CasePal project intact):

```powershell
azd ai agent delete casepal-hosted-concierge
```

📚 **Docs:** [Quickstart: Deploy your first hosted agent](https://learn.microsoft.com/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) · [Hosted agents in Foundry Agent Service](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agents) · [Author `azure.yaml`](https://learn.microsoft.com/azure/foundry/agents/how-to/deploy-hosted-agent)

---

## ✅ Checkpoint

**What you built.** An agent that calls a real external tool (the mock case-management MCP server) with approval-before-write, and a hosted version of the same agent that answers via a `/chat` endpoint.

**What CasePal did.**
- Proposed `create_case`, paused for approval, wrote to the store only after you clicked **Approve once**.
- Returned a `case_id` matching `CMS-2026-<digits>`.
- Preserved priority, follow-up owner, and condition text verbatim in the case record.
- `list_open_cases` returned the freshly-created case (and, if Part B ran, the curl-created case too — same MCP store).

**What you learned.**
- **Approvals are structured pauses.** MCP + Foundry's approval mode gives you a controllable seam between an agent's intent to write and the actual write. That's the pattern for high-consequence actions — much cleaner than "trust the model to check itself".
- **Reads don't have to require approval.** `list_open_cases` is a read; production would toggle approval off for reads. The demo leaves everything approval-required to make the flow visible.
- **Bring your own container.** The Foundry Concierge in Part B is a plain Agent Framework Python file that Foundry built into a container and now hosts — no ACA plumbing, no App Service, no FastAPI wrapper. The Responses protocol is the seam that makes this look identical from a client's perspective.
- **Model-router keeps deciding.** Router picked a cheap model for the routine lodgement and a stronger model for the reasoning turns earlier. Cost and latency track complexity with no client-side steering.

If the case_id didn't come back, check the MCP Container App logs — the tool may be pointing at a stale URL or an unhealthy endpoint.

## 🧯 Troubleshooting

- **MCP tool doesn't appear after Save?** Check the server URL — should end with `/mcp` or an SSE endpoint per the deploy notes. Refresh the tool list.
- **`create_case` fires without asking for approval?** Approval mode is set to *Auto* instead of *Required for writes*. Toggle it in the tool config.
- **Server errors on `create_case`?** Check the Container App logs. If `MCP_PERSIST_PATH` is unset the store is in-memory — restarts wipe it.
- **`list_open_cases` returns empty right after `create_case`?** Owner string mismatch — case-insensitive matching isn't enabled by default in the mock server.

---

## 🎉 End of workshop

**Previous:** [Lab 4 · Multi-Agent CasePal](lab-04.md)

You've built, grounded, governed, orchestrated, and (watched) deployed a real Foundry agent solving a
real (if synthetic) case-review workflow. If your CIO is in the room, ask them the loudest
question you've had all day.

Please give the facilitator your feedback form — including whether the pace, depth, and story landed for
your role. Every dry-run improves the next.
