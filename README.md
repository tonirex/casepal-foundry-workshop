# CasePal — Microsoft Foundry Workshop (Day One)

### *An enterprise Case Review Copilot, built on Microsoft Foundry*

A single-day, hands-on workshop where participants build **CasePal** — a case-review copilot for a
fictional regulator's registration-screening workflow — in **Microsoft Foundry**. The specific
demo domain is *medical device registration screening*, but the ten agentic patterns you learn
apply to any enterprise case-review scenario: dossier screening, investigation planning, forensic
report drafting, claim review, audit workflow, incident triage.

> [!TIP]
> **Two rails, one outcome.** Everyone builds the same CasePal agent across Labs 0→5.
> Pick the rail that matches your comfort with code — you can switch rails between labs.

---

## The ten agentic patterns you'll build

CasePal is deliberately designed to exercise the ten patterns most enterprise AI initiatives
converge on. Every lab makes at least two of them concrete:

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

**By 5:30 PM every attendee has built, grounded, governed, orchestrated, and watched deployed a working agent that exercises all ten.**

---

## Pick your rail

| Rail | For | You work in | Setup needed |
|------|-----|-------------|--------------|
| 🟢 **Navigator** | IT leaders, CIOs, strategy, non-coding IT | The **Foundry portal** (browser only) | **Nothing** — a browser + workshop login |
| 🔵 **Builder** | Developers, technical PMs, SIs | **Jupyter notebooks** (`content/assets/*.ipynb`) or auto-derived Python scripts | Codespaces *(recommended)* or local Python |

🟢 **Navigator participants need none of the setup below** — go straight to Lab 0.

---

## The story — Dr. Wei Ling's week on the review queue

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
  → *A real **tool (MCP)** into a mock case-management system, plus a **deployed**, always-on agent.*

Full narrative, one chapter per lab: [content/narrative/weiling.md](content/narrative/weiling.md).

---

## How the workshop flows

Everyone builds the **same** CasePal agent across **six labs, done in order (Lab 0 → Lab 5)**.
Each lab builds on the last, so don't skip ahead. **Start at Lab 0** — the morning equaliser everyone
does in the portal — then continue through Labs 1–5.

From Lab 1 on, every lab page is **rail-tabbed**: one page with a 🟢 Navigator and a 🔵 Builder section.
**Pick the rail that fits you and follow just that section** — you can switch rails between labs.

| Lab | Title | What you build | Patterns |
|-----|-------|----------------|----------|
| [Lab 0](content/labs/lab-00.md) | Hello, CasePal | Your first safe agent (portal, both rails) | #10 |
| [Lab 1](content/labs/lab-01.md) | Intake & Extraction | Structured JSON intake + `model-router` routing | #1, #7 |
| [Lab 2](content/labs/lab-02.md) | Knowledge & Institutional Memory | RAG over SOPs + prior cases, with citations | #4, #5, #7, #8 |
| [Lab 3](content/labs/lab-03.md) | Govern & Observe | Guardrails + evaluators + tracing | #2, #5, #7, #10 |
| [Lab 4](content/labs/lab-04.md) | Multi-Agent CasePal | Four-specialist orchestration → recommendation | #2, #3, #9 |
| [Lab 5](content/labs/lab-05.md) | Extend & Deploy | MCP case-management + hosted agent (facilitator demo) | #6, #10 |

**How to consume a lab:**
- **🟢 Navigator** — follow the portal steps in the lab page in your browser at [ai.azure.com](https://ai.azure.com).
- **🔵 Builder** — open the matching notebook (`content/assets/lab1_intake.ipynb`, Run All) or run the script (`python content/assets/lab1_intake.py`). Notebooks are the canonical Builder artefact; scripts are auto-derived via `jupyter nbconvert`.

---

## Quick start — 🔵 Builder

### Option A · GitHub Codespaces (recommended)

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

### Option B · Local machine

<details>
<summary>Windows (PowerShell)</summary>

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
<summary>macOS / Linux (bash)</summary>

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

## Access & authentication (read before the day)

The Builder rail calls a **shared Foundry project** via `DefaultAzureCredential`, so each participant
must be signed in to Azure **and** have access to that project.

**Facilitator / admin — do this *before* the workshop:**
- Grant each attendee's workshop identity the **Foundry User** role (role ID `53ca6127-db72-4b80-b1b0-d745d6d5456d`)
  on the shared Foundry resource. For a **20-person cohort**, per-attendee assignments are trivial — see
  the RBAC script under `content/admin/`.
- **Pre-deploy the models**: `model-router` + `gpt-5.5` + `gpt-5.4-mini` + `text-embedding-3-small`.
- **Pre-create the App Insights connection** for the full Lab 3 *Traces* tab.
- Share the project endpoint and model deployment names.

> [!WARNING]
> **Foundry User can't *Publish* agents.** Lab 5 Part B (hosted publish) needs **Foundry Project Manager**,
> so it is **facilitator-demo-only**. Everything else in Labs 0–5 is a *data action* that Foundry User permits.

See the [admin & logistics page](content/admin/ADMIN-SETUP.md) (with a ready-to-run RBAC script) for the full checklist.

---

## Repository map

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
    │   ├── mcp-case-management/            ← Lab 5 Part A — mock case-management MCP server
    │   ├── hosted-deploy/                   ← Lab 5 Part B — hosted-agent deploy scaffold
    │   └── case-packages.jsonl             ← 15 synthetic dossiers used across labs
    ├── knowledge/                   ← RAG grounding docs for Lab 2/4
    │   ├── sop-library/             ← 5 synthetic Agency SOPs
    │   ├── prior-cases/             ← 5 completed prior-case decisions (institutional memory)
    │   ├── references/              ← IMDRF / clinical-eval / dossier-structure / SaMD / guideline links
    │   └── fake-registry.md         ← fake product & applicant registry (collision-check policy)
    ├── narrative/weiling.md         ← the reviewer story, one chapter per lab
    ├── prompts/test-prompts.json    ← single source of truth for canned prompts + expected routes
    └── answer-keys/                 ← SERVER-SIDE validators — never ship to participants
```

> [!IMPORTANT]
> `content/answer-keys/` are **validators**, not participant assets. Keep them out of any deployed
> agent code and never surface them to the room.

---

## Synthetic-data guarantee

Every product name, applicant, dossier, MAH, and case ID in this workshop is invented. See
[`content/knowledge/fake-registry.md`](content/knowledge/fake-registry.md) for the registry and the
pre-release collision-check policy. If a name accidentally matches a real product, please open an issue.
