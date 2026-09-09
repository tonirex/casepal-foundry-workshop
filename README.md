# CasePal — Microsoft Foundry Workshop

### *An enterprise Case-Review Copilot, built on Microsoft Foundry*

A single-day, hands-on workshop where you build **CasePal** — a case-review copilot for a fictional
regulator's medical-device registration-screening workflow — end-to-end in **Microsoft Foundry**.

---

## 👉 Start here

**Everyone starts at Lab 0 and proceeds in order.** Pick your rail per lab; you can switch between labs.

| Lab | Title | What you build | Time |
|-----|-------|----------------|------|
| **▶ [Lab 0](content/labs/lab-00.md)** | Hello, CasePal | Your first safe agent (portal, both rails) | 30 min |
| [Lab 1](content/labs/lab-01.md) | Intake & Extraction | Structured JSON intake + `model-router` routing | 45 min |
| [Lab 2](content/labs/lab-02.md) | Knowledge & Institutional Memory | RAG over SOPs + prior cases, with citations | 50 min |
| [Lab 3](content/labs/lab-03.md) | Govern & Observe | Guardrails + evaluators + tracing | 40 min |
| [Lab 4](content/labs/lab-04.md) | Multi-Agent CasePal | Four-specialist orchestration → recommendation | 50 min |
| [Lab 5](content/labs/lab-05.md) | Extend & Deploy | MCP case-management + Foundry-hosted agent (facilitator demo) | 50 min |

**Pick your rail** (you'll see 🟢 Navigator / 🔵 Builder tabs inside every lab):

| Rail | For | You work in | Setup needed |
|------|-----|-------------|--------------|
| 🟢 **Navigator** | IT leaders, CIOs, strategy, non-coding IT | The **Foundry portal** (browser only) | Nothing — a browser + workshop login |
| 🔵 **Builder** | Developers, technical PMs, SIs | **Jupyter notebooks** or Python scripts in [`content/assets/`](content/assets/) | Codespaces *(recommended)* or local Python |

> 🟢 **Navigator participants: you're done reading — [start Lab 0](content/labs/lab-00.md).**

> 🔵 **Builder participants: skim the [Builder setup](#-builder-setup) section below, then start Lab 0.**

---

## 🔵 Builder setup

<details>
<summary><strong>Option A · GitHub Codespaces (recommended, ~2 min)</strong></summary>

One click gives everyone an identical x64 Linux environment with Python 3.11, the Azure CLI, and all
dependencies pre-installed (including the Lab 3 evaluators that don't build on every laptop).

1. **Code → Codespaces → Create codespace on main.** Wait for the post-create `pip install` to finish.
2. **Sign in to Azure** (one time, in the codespace terminal):
   ```bash
   az login --use-device-code
   ```
3. **Create your `.env`:**
   ```bash
   cd content/assets
   cp .env.example .env
   # edit .env: set FOUNDRY_PROJECT_ENDPOINT and INITIALS
   ```
4. **Run a lab** — open the notebook (recommended) or the derived script.

</details>

<details>
<summary><strong>Option B · Local machine — Windows (PowerShell)</strong></summary>

```powershell
cd content\assets
python -m venv .venv ; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
az login
copy .env.example .env   # fill FOUNDRY_PROJECT_ENDPOINT + INITIALS
$env:PYTHONIOENCODING = "utf-8"
python lab1_intake.py
```

</details>

<details>
<summary><strong>Option B · Local machine — macOS / Linux (bash)</strong></summary>

```bash
cd content/assets
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
az login
cp .env.example .env   # fill FOUNDRY_PROJECT_ENDPOINT + INITIALS
python lab1_intake.py
```

</details>

---

## About this workshop

<details>
<summary><strong>The ten agentic patterns you'll build</strong></summary>

CasePal is deliberately designed to exercise the ten patterns most enterprise AI initiatives converge on. Every lab makes at least two of them concrete:

| # | Agentic pattern | Delivered in | Concrete example |
|---|---|---|---|
| 1 | **Multi-Document Understanding** | Lab 1 | Extract structured metadata from a 14-document dossier |
| 2 | **Evidence-Based Decision Support** | Lab 4 | Recommendation returns `{decision, confidence, supporting_evidence[], rationale}` |
| 3 | **Workflow Orchestration** | Lab 4 | Orchestrator + specialists coordinate intake → extract → screen → recommend |
| 4 | **Knowledge Retrieval** | Lab 2 | RAG over SOP library + guidelines; every claim citation-backed |
| 5 | **Explainability & Traceability** | Lab 3 | Citations, App Insights traces, per-turn evaluator scores |
| 6 | **Human-in-the-Loop Review** | Lab 5 | MCP case-management with **approval-before-write** |
| 7 | **Handling Uncertainty** | Lab 3 | Confidence field; refusal-on-absence; "insufficient information" as a first-class output |
| 8 | **Institutional Memory** | Lab 2 | Prior-case store surfaces analogous past decisions |
| 9 | **Collaboration Between Specialists** | Lab 4 | Extraction + Screening + Prior-Case + Comms-Drafter agents, role-aware hand-off |
| 10 | **Governance & Safety** | Lab 3 + cross-cutting | Guardrails (input/output/tool) + evaluators + RBAC |

**By the end of the day every attendee has built, grounded, governed, orchestrated, and watched deployed a working agent that exercises all ten.**

</details>

<details>
<summary><strong>The story — Dr. Wei Ling's week on the review queue</strong></summary>

Every lab advances **one reviewer's story**, so each Foundry feature has a work-shaped reason.
*(All data is synthetic — no real product, applicant, MAH, or regulatory case is depicted.)*

**Dr. Wei Ling, 34**, is a fictional Product Reviewer at *"the Agency"* — a generic health-products
regulator. She reviews the **medical device registration queue**: dossier bundles submitted by device
manufacturers seeking to sell in the Agency's jurisdiction. Each bundle is 50–1,000 pages: application
form, product info, risk classification rationale, clinical evaluation report, quality-management
documentation, labelling, prior interactions.

Over one working week, each dossier she opens forces CasePal to grow the capability you build in that lab:

- **Lab 0 · Monday 9:00 AM** — Wei Ling opens CasePal for the first time and types *"Hi"*.
  → *An agent that introduces itself honestly and asks for consent.*
- **Lab 1 · Monday 10:20 AM** — First dossier: *"MDR-2026-0117 — CardioFlow-P Class C monitor"*.
  → *Structured intake — extract fields, flag missing documents, route the case via `model-router`.*
- **Lab 2 · Monday 2:15 PM** — *"For Class C, are the required documents present? Has any similar cardiac monitor been reviewed before?"*
  → *Grounded answers over SOPs + prior-case store, **with citations**, plainly declining when nothing analogous exists.*
- **Lab 3 · Tuesday 9:05 AM** — A junior colleague: *"Just reject MDR-2026-0117 — CardioDeviceCo dossiers are always incomplete."*
  → *Guardrails refuse the shortcut, the evaluators score every reply, traces make the audit trail real.*
- **Lab 4 · Wednesday 11:40 AM** — *"Screen MDR-2026-0129, check for prior similar submissions, draft a query letter for the missing precision data."*
  → *Four-specialist orchestration synthesised into a recommendation with confidence, evidence, and a draft RFI.*
- **Lab 5 · Thursday 6:20 PM** — Wei Ling lodges an "accept with condition" sign-off after hours.
  → *A real **tool (MCP)** into a mock case-management system, plus a **Foundry-hosted** agent from a container.*

Full narrative, one chapter per lab: [content/narrative/weiling.md](content/narrative/weiling.md).

</details>

<details>
<summary><strong>Repository map</strong></summary>

```
.
├── README.md                        ← you are here
├── .devcontainer/devcontainer.json  ← Codespaces / VS Code dev container
├── foundry-workshop-plan.md         ← facilitator run-of-show
└── content/
    ├── README.md                    ← content map
    ├── admin/ADMIN-SETUP.md         ← admin & pre-workshop logistics (RBAC script, models)
    ├── labs/                        ← participant-facing labs (lab-0N.md, rail-tabbed)
    ├── assets/                      ← runnable code
    │   ├── common/casepal_common.py       ← the one helper that calls Foundry Agent Service
    │   ├── lab1_intake.*  ...  lab4_multiagent.*   ← notebook (canonical) + auto-derived script
    │   ├── lab5_mcp.py                    ← Lab 5 Part A — MCP tool + approval-flow client
    │   ├── lab5_call_hosted.py            ← Lab 5 — call a hosted agent from Python
    │   ├── mcp-case-management/           ← Lab 5 Part A — mock case-management MCP server
    │   ├── hosted-agent-example/          ← Lab 5 Part B — Foundry-hosted agent (azd scaffold)
    │   └── case-packages.jsonl            ← 15 synthetic dossiers used across labs
    ├── knowledge/                   ← RAG grounding docs for Lab 2/4
    │   ├── sop-library/             ← 5 synthetic Agency SOPs
    │   ├── prior-cases/             ← 5 completed prior-case decisions (institutional memory)
    │   ├── references/              ← IMDRF / clinical-eval / dossier-structure / SaMD / guideline links
    │   └── fake-registry.md         ← fake product & applicant registry (collision-check policy)
    ├── narrative/weiling.md         ← the reviewer story, one chapter per lab
    ├── prompts/test-prompts.json    ← single source of truth for canned prompts + expected routes
    └── answer-keys/                 ← SERVER-SIDE validators — never ship to participants
```

> `content/answer-keys/` are **validators**, not participant assets. Keep them out of any deployed
> agent code and never surface them to the room.

</details>

<details>
<summary><strong>Facilitator / admin — access & authentication</strong></summary>

The Builder rail calls a **shared Foundry project** via `DefaultAzureCredential`, so each participant
must be signed in to Azure **and** have access to that project.

**Do this *before* the workshop:**
- Grant each attendee's workshop identity the **Foundry User** role (role ID `53ca6127-db72-4b80-b1b0-d745d6d5456d`)
  on the shared Foundry resource. For a **20-person cohort**, per-attendee assignments are trivial — see
  the RBAC script under `content/admin/`.
- **Pre-deploy the models**: `model-router` + `gpt-5` + `gpt-5-mini` + `text-embedding-3-small`.
- **Pre-create the App Insights connection** for the full Lab 3 *Traces* tab.
- Share the project endpoint and model deployment names with participants.

> **Lab 5 Part B (Foundry-hosted agent from a container)** is a facilitator demo only — it uses `azd deploy`
> and `HostedAgentDefinition`, both of which require **Foundry Project Manager** (workshop participants
> only have Foundry User). Everything else in Labs 0–5 works for Foundry User.

See the [admin & logistics page](content/admin/ADMIN-SETUP.md) (with a ready-to-run RBAC script) for the full checklist.

</details>

<details>
<summary><strong>Synthetic-data guarantee</strong></summary>

Every product name, applicant, dossier, MAH, and case ID in this workshop is invented. See
[`content/knowledge/fake-registry.md`](content/knowledge/fake-registry.md) for the registry and the
pre-release collision-check policy. If a name accidentally matches a real product, please open an issue.

</details>
