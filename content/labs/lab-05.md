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
- **Part B** — hosted publish. 👀 **Facilitator demo only** (RBAC — Foundry User cannot Publish).

## Demo (facilitator, 5 min)

Show the mock case-management MCP server running (Azure Container Apps). In a fresh chat, send Wei Ling's
lodgement request → CasePal picks the MCP tool, prompts for **approval before write**, Wei Ling
confirms, MCP returns `CMS-2026-1188`. Then show the same behaviour from the published hosted agent
endpoint via `curl`.

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

**Facilitator setup (already done for you):** deployed to Azure Container Apps via
`deploy-mcp.sh` (bash) or `deploy-mcp.ps1` (PowerShell). The endpoint URL is on the workshop info sheet.

### 🔵 Builder — connect the tool

1. Reuse your **`casepal-<initials>-knowledge`** (or clone it as `casepal-<initials>-mcp`). Update its Instructions to reference the MCP tool:

   ![MCP-connected agent Instructions showing 'When the reviewer asks to lodge a case decision, use the casepal-case-management MCP tool. Confirm approval BEFORE any create_case or update_case_status call.'](screenshots/lab-05/nav-01-instructions.png)

2. In the portal, open **Tools & Knowledge** → **+ Add MCP tool**.
3. Enter:
   - **Server URL**: (facilitator provides — looks like `https://casepal-mcp-<hash>.azurecontainerapps.io`)
   - **Auth**: **None** for demo (real deployment would use Managed Identity).
   - **Approval mode**: **Required for writes** — this is the "always confirm before create/update" contract.
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

8. **Note the returned `case_id`** (looks like `CMS-2026-<n>`). You'll use it in the next section — the **✅ Checkpoint** — to self-check the whole approval flow end-to-end.

### Behind the scenes (script rail)

`content/assets/lab1_intake.py` and friends provide the Builder rail. Lab 5's code is in the MCP server itself
(`mcp-case-management/server.py`) plus an `agent_client.py` script (in `hosted-deploy/src/`) that
demonstrates calling a hosted CasePal from Python.

📚 **Docs:** [MCP tools in Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/mcp) · [Approval workflow for write operations](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/mcp#approval-workflow)

---

## Part B — Hosted publish (👀 facilitator demo)

> [!WARNING]
> **This part is a facilitator demo, not participant hands-on.** Publishing a hosted agent requires
> **Foundry Project Manager** at the Foundry resource scope. Workshop participants only have **Foundry
> User** (RBAC-limited). The facilitator's identity has the extra role.

The facilitator will:
1. Open `content/assets/hosted-deploy/`.
2. Run `azd up` (Azure Developer CLI) — provisions an Azure Container Apps hosted-agent endpoint that
   loads the same `casepal-<initials>-mcp` agent definition.
3. Show a `curl` call against the hosted endpoint:
   ```bash
   curl -X POST "$AGENT_ENDPOINT/chat" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Lodge MDR-2026-0135 to case management as accept with condition"}]}'
   ```
4. Show the returned case_id **matching** what you got in Part A — same agent, same MCP tool, same store.

   ![Terminal-styled transcript: /healthz sanity check, then POST /chat with the lodgement JSON payload, response returned in 20.3s with case_id CMS-2026-1188; ends with 'Hosted endpoint returned CMS-2026-1188 — same behaviour, programmatic access'](screenshots/lab-05/99-curl-hosted-terminal.png)

The point isn't *publishing* (which you'd wire into a real product yourselves); it's that **once your
agent works in the portal, it's the same object accessible via API for downstream integration**. Notice
that the Part A portal `list_open_cases` result above includes both this curl case (CMS-2026-1188)
and the portal case (CMS-2026-1190) — visual proof that they hit the same MCP store.

📚 **Docs:** [Hosted agents on Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/deploy-hosted)

---

## ✅ Checkpoint — reflect on what you observed

Nothing to paste. Look at the returned `case_id`, the trace of the lodgement turn, and the `list_open_cases` output. Confirm the behaviours below.

**What you should have observed**

- **The returned case_id matches `CMS-2026-<digits>`** — a real record in the mock case-management store.
- **`get_case(<your_id>)` returns a case** with `priority: "medium"` and `follow_up_owner` set to what you provided (`wl@agency-demo.test`). The condition text is preserved verbatim in the note.
- **The trace shows an approval step was surfaced and confirmed before the write.** You should see the `create_case` proposal, a *Request pending approval* signal, then the `Request has been approved` marker, then the tool result. If the write happened without an approval step, the Approval mode setting is *Auto* — flip it to *Required for writes* and try again.
- **`list_open_cases` returned your just-created case.** If the facilitator ran the Part B curl demo earlier, that case is in the same list too — visual proof that portal chat and the hosted API hit the same store.

**Learning points**

- **Approvals are just structured pauses.** MCP + Foundry's approval mode gives you a controllable seam between an agent's *intent to write* and the *actual write*. That's the design pattern for high-consequence actions — much cleaner than "trust the model to check itself".
- **Reads don't have to require approval.** `list_open_cases` is a read; in a production deployment you'd toggle its approval requirement off. The demo leaves them all approval-required so the flow is visible.
- **Hosting doesn't change the agent.** The same agent-reference works from a hosted `/chat` endpoint, from the portal, from a notebook, and from a downstream integration. The MCP tool, the approval semantics, and the Foundry evaluators come along for free.
- **Model-router keeps deciding.** For a routine lodgement, router likely picked a fast model. For a complex reasoning turn earlier in the day, it may have picked `gpt-5.6-luna`. Cost and latency track complexity without any client-side steering.

If the case_id didn't come back, look at the MCP server logs (Container App Log stream) — the MCP tool may be pointing at a stale URL or an unhealthy endpoint.

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
