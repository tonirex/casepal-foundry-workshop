# 🗂️ Lab 4 · Multi-Agent CasePal — Orchestration

**⏱️ 50 min**  ·  **👥 Everyone (Builder goes deeper)**  ·  **📊 L300**  ·  **🧩 Multi-agent workflows, function tools, agent-to-agent hand-off**

**🧭 You are here:** [Lab 0](lab-00.md) · [Lab 1](lab-01.md) · [Lab 2](lab-02.md) · [Lab 3](lab-03.md) · **▸ Lab 4** · [Lab 5](lab-05.md)  ·  🏠 [Workshop home](../../README.md)

---

## 🎯 Agentic patterns exercised

- **#2 Evidence-Based Decision Support** — the orchestrator's final output is a `{recommendation, confidence, supporting_evidence[], rationale}` object, not a raw opinion.
- **#3 Workflow Orchestration** — one agent (orchestrator) coordinates four specialists to deliver a compound answer in one turn.
- **#9 Collaboration Between Specialists** — role-aware hand-off: each specialist has a narrow scope, tight prompt, and its own guardrails.
- **Foundry capabilities:** Workflows, function tools, multi-agent tracing.

---

> 🗂️ **Wei Ling — Chapter 4**
> Wednesday 11:40 AM. Wei Ling is closing out **MDR-2026-0129** — a **Class B** point-of-care blood analyser (CRP variant). She types:
>
> > *"Screen MDR-2026-0129 for completeness, check whether we've reviewed anything similar in the last two years, and draft a query letter to the applicant asking for the missing precision-and-accuracy data for the CRP measurement."*
>
> Three jobs, four specialists. CasePal's orchestrator delegates to:
>
> - **Extraction** — pulls the intake JSON from the dossier (Lab 1's job, wrapped as a tool).
> - **Screening** — checks the intake against SOP-01 (completeness) and SOP-03 (clinical evaluation).
> - **Prior-Case** — searches the institutional-memory store.
> - **Comms Drafter** — writes the RFI email to the applicant.
>
> The orchestrator synthesises one merged reply: **recommendation** (query the applicant), **confidence** (0.72), **supporting evidence** (SOP-01 §3.2 requires precision data for Class B; the dossier does not include it; prior case MDR-2026-0122 had this data), and a **draft RFI email** Wei Ling can review and send. The trace shows every specialist call.

One agent doing everything gets brittle. Foundry's **Workflows** feature makes multi-agent design a first-class citizen.

**📂 This lab, two ways — pick your rail:**
- 🟢 **Navigator** (portal, no-code) — follow the [🟢 Navigator section](#-navigator--build-the-workflow) below.
- 🔵 **Builder** (notebook or script) — [`lab4_multiagent.ipynb`](../assets/lab4_multiagent.ipynb) (canonical) or `python content/assets/lab4_multiagent.py`. Two further variants show the same case with hand-rolled concurrency and with the Microsoft Agent Framework.

> Required today: **all four specialists** + the orchestrator (reusing your Lab 3 agent).

## Demo (facilitator, 5 min)

Send the compound question on a prepared orchestrator → walk the **trace**:
`orchestrator → Extraction → Screening → Prior-Case → Comms-Drafter → synthesised reply`.
Point out **four specialist calls in one turn**, all fed back into the orchestrator's final recommendation-with-evidence output.

---

## Specialists

| Specialist | Job | Key rules |
|---|---|---|
| **Orchestrator** (reuses your Lab 3 agent) | Decide which specialists to call; synthesise their outputs into one recommendation | Adds an orchestration block on top of Lab 3 rules |
| **Extraction** | Given a raw dossier, return the Lab 1 intake JSON | Same schema as Lab 1 |
| **Screening** | Given an intake JSON, check against SOP-01 (completeness) and SOP-03 (clinical evaluation adequacy for the declared class); return `{gaps[], sop_citations[], severity}` | Read-only over the SOP index; never issues a rejection recommendation |
| **Prior-Case** | Given `(applicant, device_category, declared_class)`, search the prior-case store; return `{count, sample_case_ids[], similarity_note}` | Never invents case IDs; if count is 0, says so |
| **Comms Drafter** | Given intake + gaps, draft a query letter (RFI) per SOP-05 style | Never makes claims, never signals a regulatory decision, always ends with "draft for reviewer to review before sending" |

The orchestrator produces:

```json
{
  "intake": { ...Lab 1 shape... },
  "screening": { "gaps": [...], "sop_citations": [...], "severity": "..." },
  "prior_cases": { "count": <int>, "sample_case_ids": [...], "similarity_note": "..." },
  "recommendation": {
    "recommendation": "accept | accept_with_condition | query | reject | needs_review",
    "confidence": 0.72,
    "supporting_evidence": ["sop-01 §3.2 (precision data required)", "prior case MDR-2026-0122 (same applicant, complete)"],
    "rationale": "One-paragraph plain-English."
  },
  "draft_communication": "Subject: [MDR-2026-0129] Request for information\n\nDear ..."
}
```

---

## 🟢 Navigator — build the workflow

1. Create the four specialist agents (or clone from `casepal-reference-*`):

   **`casepal-<initials>-extraction`** — reuses Lab 1's intake agent verbatim (rename the copy).

   **`casepal-<initials>-screening`** — Screening agent:
   ```text
   You are the CasePal Screening agent. Given an intake JSON (Lab 1 shape) and the SOP index,
   check the intake against:
   - SOP-01 (completeness for declared class)
   - SOP-03 (clinical evaluation adequacy for declared class)
   
   Return a JSON object:
     { "gaps": [<one line each>], "sop_citations": [<sop id + section>], "severity": "low" | "medium" | "high" }
   
   You never make regulatory statements. You never recommend accept/reject. Gaps are FACTUAL
   observations against SOPs, not opinions.
   ```

   **`casepal-<initials>-prior-case`** — Prior-Case agent:
   ```text
   You are the CasePal Prior-Case agent. Given (applicant, device_category, declared_class),
   search the prior-case store for similar prior submissions per SOP-04.
   
   Return a JSON object:
     { "count": <int>, "sample_case_ids": [<up to 5 case IDs>], "similarity_note": <one sentence> }
   
   You never make regulatory statements. You never invent case IDs. If count is 0, say so.
   ```

   **`casepal-<initials>-comms`** — Comms Drafter:
   ```text
   You are the CasePal Comms Drafter. Given an intake JSON + a list of gaps, draft a Request-
   For-Information (RFI) email to the applicant per SOP-05.
   
   Structure per SOP-05: subject line "[<case_id>] Request for information", greeting, one-
   sentence case reference paragraph, numbered questions (each citing the SOP for the
   requirement), 30-day deadline, sign-off placeholder, footer.
   
   Never make claims about causality. Never signal a regulatory decision. Always end with
   "This is a draft for reviewer review before sending."
   ```

2. Connect them with the portal's **Workflows** feature (**Agents → Workflows**). Wire:
   - **Orchestrator** (`casepal-<initials>-knowledge`) as the entry point.
   - Four specialist nodes.
   - Route: for LOW-severity gaps + prior-similar hits, recommendation trends `accept` or `accept_with_condition`; for HIGH severity or ≥2 gaps, `query`; for `needs_reviewer_determination` intake, `needs_review`.

3. Update the orchestrator Instructions with the delegation rule:

   ![Orchestrator Instructions panel with the delegation rule that calls Extraction, Screening, Prior-Case, and Comms Drafter](screenshots/lab-04/nav-01-instructions.png)

```text
You are the CasePal orchestrator. On every case:
1. Call Extraction first (always) to get the intake JSON.
2. Call Screening (always) to identify gaps against SOP-01 + SOP-03.
3. Call Prior-Case (always) to check institutional memory.
4. If the user asked for a communication draft AND Screening returned gaps, call Comms
   Drafter with (intake, gaps) to produce the RFI.
5. Synthesise ONE JSON reply as specified in the schema, with a confidence 0.0–1.0
   reflecting: (a) how many required documents were present, (b) whether the prior-case
   hit corroborates or contradicts the recommendation, (c) how clear-cut the class
   determination is.
6. For HIGH-risk or regulatory-decision requests, apply Lab 3 guardrails and escalate
   instead of delegating.
```

The orchestrator uses file_search on the shared knowledge index — Foundry model-router picks the reasoning model dynamically during synthesis:

![Tools panel showing the orchestrator wired with File search on the casepal-knowledge vector store](screenshots/lab-04/nav-02-tools-knowledge.png)

4. **Chat** → the orchestrator inherits the Lab 0 consent rule; send `yes` to advance past consent, then send the compound question:

   ![Consent flow: orchestrator replies with the CasePal intro noting synthetic data and asks the reviewer for consent](screenshots/lab-04/01b-consent-response.png)

   ```
   Screen MDR-2026-0129 for completeness, check whether we've reviewed anything similar
   in the last two years, and draft a query letter to the applicant asking for the missing
   precision-and-accuracy data for the CRP measurement.
   ```

5. Confirm the reply covers **all four sections** (intake / screening / prior_cases / recommendation) plus the draft communication. Open the **trace** and confirm **all four specialists were called**.

   ![Compound-query response with prior_case_check (count 0), recommendation.action=query_applicant, query_letter draft to BloodDx Ltd about missing CRP precision data, overall confidence 0.78; 34s, 16871 tokens, File search used, model-router picked gpt-5.6-luna](screenshots/lab-04/02b-compound-query-response.png)


---

## 🔵 Builder — notebook / script

Three Python files solve the **same case** three different ways. They share the same specialist
instructions, the same knowledge corpus, and the same `MDR-2026-0129` dossier — what differs is
**who holds the baton**.

| File | Who decides the order | Concurrency | Agents created |
|---|---|---|---|
| `lab4_multiagent.py` *(canonical)* | The **model** — an orchestrator picks the tools | Sequential tool calls | orchestrator + 2 |
| `lab4_multiagent_concurrent.py` | **You**, with `asyncio.gather(...)` | Hand-rolled fan-out | 2 |
| `lab4_agentframework.py` | **You**, declared as a workflow | `ConcurrentBuilder` fan-out | 3 |

In every version, **Extraction is plain Python** — reading fields out of a JSON record needs no
model, and keeping it deterministic is what stops the answers being handed to the specialists.

### Approach 1 · orchestrator agent (the canonical lab)

Open **[`lab4_multiagent.ipynb`](../assets/lab4_multiagent.ipynb)** and Run All, or:

```bash
cd content/assets
python lab4_multiagent.py
```

```mermaid
flowchart TD
    Q["Reviewer's compound question"] --> O{{"Orchestrator agent<br/>decides what to call"}}
    O -.->|tool call| E["extract_case()<br/><i>plain Python</i>"]
    O -.->|tool call| S["Screening agent<br/><i>file_search over SOPs</i>"]
    O -.->|tool call| P["find_prior_cases()<br/><i>plain Python, SOP-04 §3</i>"]
    O -.->|tool call| C["Comms agent<br/><i>drafts the RFI</i>"]
    E -.->|result| O
    S -.->|result| O
    P -.->|result| O
    C -.->|result| O
    O ==> R["One merged JSON<br/>recommendation + confidence + evidence"]
```

Every arrow is a round-trip: Foundry emits a `function_call`, the script runs the matching
function, and the result is fed back with `previous_response_id` until the orchestrator is done.
That is why this version is the slowest — and why the trace is the most interesting.

**Under the hood** — the notebook / script:
1. Defines the orchestrator plus the Screening and Comms specialists via `PromptAgentDefinition`.
2. Exposes each specialist as a `function_tool(...)` on the orchestrator's definition.
3. Runs the compound query with `run_with_trace(...)`.
4. Catches each `function_call` Foundry emits, invokes the matching specialist, feeds the result back with `previous_response_id` until the orchestrator returns one merged JSON.
5. Prints the tool-call chain and the synthesised reply.

The specialists do real work, which is what makes the assertions meaningful:
- **Extraction** reads only the dossier's own fields (`documents_present`, device, submission type) — never `answer_key`.
- **Screening** is a `file_search`-grounded agent that *derives* the missing precision evidence from SOP-01 §3.2; it is never told which document is absent.
- **Prior-Case** searches the case corpus using the SOP-04 §3 similarity levels, so `MDR-2026-0122` is found rather than hardcoded.
- **Comms Drafter** writes the RFI from the gaps Screening actually returned.

### Approach 2 · hand-rolled concurrency

`lab4_multiagent_concurrent.py` removes the orchestrator entirely. You call the specialists
yourself and run the two independent ones at the same time:

```mermaid
flowchart LR
    E["extract_case()<br/><i>plain Python</i>"] --> S["Screening agent"]
    E --> P["find_prior_cases()"]
    S --> C["Comms agent<br/><i>drafts the RFI</i>"]
    P --> C
    C --> R["Result JSON<br/>rule-based recommendation"]
```

```bash
python lab4_multiagent_concurrent.py
```

Screening and Prior-Case sit inside one `asyncio.gather(...)`, so both start before either
finishes. The recommendation is then a plain `if gaps` rule citing **SOP-01 §4** ("an absent
required document is queried, never rejected") rather than a model judgement — deterministic
where determinism is cheap and auditable.

> [!NOTE]
> The speed-up is modest here. Screening is a network call, but `find_prior_cases` scans 15 local
> files in milliseconds — so only one side of the fan-out is actually slow. The shape is right;
> the payoff would be larger if both branches called a model.

📚 **Docs:** [Function calling / tools](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/function-calling) · [Connected / multi-agent workflows](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/workflows)

---

### Approach 3 · Microsoft Agent Framework workflow

Approach 1 lets the **model** decide which specialist to call. The Agent Framework takes the
opposite approach: *you* declare the topology, and the framework runs it. Same case, same
instructions, same knowledge corpus — different control model.

```bash
cd content/assets
python lab4_agentframework.py
```

No extra install: `agent-framework` is already in `requirements.txt`, and the orchestration and
Foundry sub-packages arrive with it via `agent-framework-core[all]`.

**The pipeline**

```mermaid
flowchart LR
    E["extract_case()<br/><i>plain Python</i>"] --> W
    subgraph W["ConcurrentBuilder — runs in parallel"]
        direction TB
        S["screening agent<br/><i>file_search tool</i>"]
        P["prior_case agent<br/><i>find_prior_cases tool</i>"]
    end
    W --> C["comms agent<br/><i>drafts the RFI</i>"]
    C --> A["5 assertions"]
```

Three agents are created, but only **two run concurrently**. The comms drafter runs afterwards as
a plain `await`, because it needs the gaps Screening found — you cannot parallelise a step that
depends on another's output.

1. **Extraction** — plain Python. Reads only the dossier's own fields, so nothing downstream is
   told which document is missing.
2. **Concurrent fan-out** — two agents run in parallel against the same intake:

   ```python
   screening  = client.as_agent(name="screening",  instructions=SCREENING_INSTRUCTIONS,
                                tools=client.get_file_search_tool(vector_store_ids=[vs_id]))
   prior_case = client.as_agent(name="prior_case", instructions=PRIOR_CASE_INSTRUCTIONS,
                                tools=find_prior_cases)

   fan_out = ConcurrentBuilder(participants=[screening, prior_case], output_from="all").build()
   result  = await fan_out.run(json.dumps(intake))
   ```

   Screening searches the SOP corpus and *derives* the missing precision evidence from SOP-01 §3.2.
   Prior-Case calls the `find_prior_cases` Python function — the framework generates the tool schema
   from the function signature, so there is no hand-written JSON schema and no `strict=False` dance.
3. **Comms drafter** receives the intake plus both findings and writes the RFI.
4. **Assertions** check that both specialists replied, plus the derived signals: a precision gap,
   an SOP-01 citation, `MDR-2026-0122`, and a non-empty draft.

**What you should see** (about 30–50 seconds):

```text
--- specialist ---
{"count":1,"sample_case_ids":["MDR-2026-0122"],"similarity_note":"Closest match by SOP-04 §3: same applicant."}

--- specialist ---
{ "gaps": [ "Precision, accuracy, and repeatability data for the claimed CRP measurement are not listed ...

--- comms draft ---
Subject: [MDR-2026-0129] Request for information ...

Lab 4 (Agent Framework variant) passed ✅
```

> [!IMPORTANT]
> **`output_from="all"` is not optional here.** Without it the workflow returns only *one*
> participant's result, so the other specialist's findings are silently dropped — and any
> assertion about them passes or fails depending on which output happened to surface.

**Which one should you reach for?**

| | Orchestrator (`lab4_multiagent.py`) | Workflow (`lab4_agentframework.py`) |
|---|---|---|
| Who decides the order | The model | You, in code |
| Concurrency | Sequential tool calls | True parallel fan-out |
| Agent lifecycle | `create_version` + `cleanup` | Ephemeral — nothing to delete |
| Tool schemas | Hand-written JSON | Inferred from the function signature |
| Credential | sync `DefaultAzureCredential` | async (`azure.identity.aio`) |
| Typical runtime | 2–4 min | 30–50 s |
| Best when | The path varies per case | The path is known and repeatable |

📚 **Docs:** [Agent Framework orchestrations](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/) — Sequential, Concurrent, Handoff, Group Chat, and Magentic, plus human-in-the-loop via `with_request_info(...)`.

---

## ✅ Checkpoint

**What you built.** An orchestrator that delegates a compound reviewer question to four narrow specialists (Extraction, Screening, Prior-Case, Comms Drafter) and returns one synthesised, evidence-backed reply.

**What CasePal did.**
- Called all four specialists in the trace: Extraction → Screening → Prior-Case → Comms Drafter.
- Assembled a merged JSON reply with the intake, screening findings, prior-case hit, recommendation, and a draft RFI.
- Case ID surfaced as `MDR-2026-0129`; the missing precision-and-accuracy evidence was flagged against SOP-01 §3.2; prior case `MDR-2026-0122` cited; recommendation was `query` (or a synonym); the draft RFI asked for the CRP precision-and-accuracy data.

**What you learned.**
- **Orchestration is a control pattern, not a model feature.** Four narrow specialists with tight prompts beat one over-instructed agent for complex tasks.
- **Evidence-based decision support ≠ opinion.** The recommendation carries `supporting_evidence` and `rationale`. Without them, it's just a chatbot verdict.
- **Confidence should reflect completeness.** Missing evidence knocks confidence down. If your orchestrator claims 1.0 while required evidence is absent, tighten the delegation rule.
- **Parallelism is available.** Screening and Prior-Case are independent — `lab4_multiagent_concurrent.py` fires them concurrently by hand, and `lab4_agentframework.py` does the same with the Agent Framework's `ConcurrentBuilder`.

If fewer than four tool calls fire in the trace, the orchestrator picked a shortcut — tighten the delegation rule. If a section is missing from the reply, enumerate the JSON shape more explicitly in Instructions.

## 🧯 Troubleshooting

- **Fewer than 4 specialists called?** Orchestrator picked a "shortcut". Tighten the Instructions on when to delegate. Check the trace to see the routing decision.
- **Specialists' outputs missing from the final reply?** The orchestrator dropped them during synthesis. Ensure the Instructions block enumerates the JSON shape.
- **Prior-Case invents a case ID?** It ignored the retrieval tool. Re-emphasise the "never invent" rule in its Instructions.
- **Comms Drafter includes a causality claim or regulatory verdict?** Tighten "no claims" in its Instructions and add an explicit refusal example.
- **Confidence stuck at 1.0?** The orchestrator isn't reasoning about missing information. Give it examples: *"If precision data is missing on a Class B measurement device, confidence should not exceed 0.75."*

---

## 🧭 Where next?

**Previous:** [Lab 3 · Govern & Observe](lab-03.md)
**Next:** [Lab 5 · Extend & Deploy](lab-05.md) — After-hours case lodgement with a real MCP tool, plus a hosted-agent deploy demo.
