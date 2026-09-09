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
- 🔵 **Builder** (notebook or script) — [`lab4_multiagent.ipynb`](../assets/lab4_multiagent.ipynb) (canonical) or `python content/assets/lab4_multiagent.py`. A concurrent-execution variant lives in `lab4_multiagent_concurrent.py`.

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

## 🟢 Navigator — connect the specialists

The four specialists (`casepal-<initials>-extraction`, `-screening`, `-prior-case`, `-comms`) are already created for you as separate Foundry agents. Your job is to wire the orchestrator so it can call them as tools.

**A note on Foundry Workflows.** The portal has a **Workflows** feature (**Agents → Workflows**) that historically hosted this pattern. Microsoft is retiring Workflows on **1 December 2026** in favour of the **Microsoft Agent Framework**. This lab therefore uses the current recommended path: connect each specialist to the orchestrator as an **Agent-to-agent (A2A)** tool.

1. Confirm the four specialist agents exist in your project (**Agents** list).

2. Open your **`casepal-<initials>-knowledge`** agent (from Lab 2 / Lab 3) — this is the orchestrator.

3. Update the orchestrator's Instructions with the delegation rule:

   ![Orchestrator Instructions panel with the delegation rule that calls Extraction, Screening, Prior-Case, and Comms Drafter](screenshots/lab-04/nav-01-instructions.png)

   ```text
   You are the CasePal orchestrator. On every case:
   1. Call the Extraction specialist first to get the intake JSON.
   2. Call the Screening specialist to identify gaps against SOP-01 + SOP-03.
   3. Call the Prior-Case specialist to check institutional memory.
   4. If the user asked for a communication draft AND Screening returned gaps, call the
      Comms Drafter with (intake, gaps) to produce the RFI.
   5. Synthesise ONE JSON reply with sections: intake, screening, prior_cases,
      recommendation (with recommendation, confidence 0.0-1.0, supporting_evidence[],
      rationale), draft_communication.
   6. For HIGH-risk or regulatory-decision requests, apply Lab 3 guardrails.
   ```

4. Under **Tools & Knowledge**, click **Add → Add tools → Custom → Agent2agent (A2A)**. Add one entry per specialist. The dialog asks for a name, an A2A endpoint, and authentication (Microsoft Entra Agent Identity).

   ![A2A tool config dialog: Connect the A2A Tool with a name field, an A2A Agent Endpoint field expecting a URL like https://api.box.com/a2a, and Authentication set to Microsoft Entra Agent Identity. A note explains the calling agent needs the 'Foundry Agent Consumer' role assigned when connecting to another Foundry agent.](screenshots/lab-04/nav-03-a2a-config.png)

   > 💡 **A2A requires each specialist to be published as an A2A endpoint.** Foundry doesn't auto-expose agents as A2A servers today; publishing is a facilitator task in a real environment. In this workshop we use the equivalent **function-tool orchestration** pattern from the Builder rail as the practical implementation — see below.

5. **Chat** → send the compound question:

   ```
   Screen MDR-2026-0129 for completeness, check whether we've reviewed anything similar
   in the last two years, and draft a query letter to the applicant asking for the missing
   precision-and-accuracy data for the CRP measurement.
   ```

6. Confirm the reply covers **all five sections** (intake, screening, prior_cases, recommendation, draft_communication). Open the **Traces** tab and confirm **all four specialists were called** — not one agent that produced a JSON that *looks* multi-agent.

---

## 🔵 Builder — function-tool orchestration (the real multi-agent path)

Because A2A currently requires each specialist to be published as an endpoint, this workshop teaches multi-agent via **function tools** in the Foundry Agent SDK. Each tool is a Python handler that dispatches to a deployed specialist agent using the same `agent_reference` pattern from Lab 2. Under the hood this is identical to A2A: an orchestrator sends work to another agent, gets a reply back, and continues its own turn.

Open **[`lab4_multiagent.ipynb`](../assets/lab4_multiagent.ipynb)** and Run All, or:

```bash
cd content/assets
python lab4_multiagent.py
```

**Under the hood** — the notebook / script:
1. Defines the orchestrator with four `function_tool(...)` definitions: `extract_case`, `screen_case`, `find_prior_cases`, `draft_rfi`.
2. Each tool handler forwards the call to the corresponding deployed specialist (`casepal-<initials>-{extraction,screening,prior-case,comms}`) via the responses API.
3. The orchestrator runs the compound query; each time it emits a `function_call`, the runner catches it, invokes the specialist, and feeds the result back using `previous_response_id`.
4. The chain terminates when the orchestrator produces the synthesised JSON.

A concurrent variant (`lab4_multiagent_concurrent.py`) shows how to run Screening + Prior-Case + Comms Drafter in parallel via `asyncio.gather(...)` once Extraction returns — the three downstream specialists are independent.

**Sample run showing the real trace:**

![Cinematic terminal transcript of demo-lab4-real-multiagent.py: orchestrator issues 4 function calls to casepal-demo-extraction, casepal-demo-screening, casepal-demo-prior-case, and casepal-demo-comms; each specialist returns real JSON output; orchestrator synthesises intake + screening (severity high, 4 gaps, SOP-01/SOP-03 citations) + prior_cases (count 0, no prior similar) + recommendation (confidence 0.55, 5 pieces of supporting evidence) + draft_communication (9-point RFI); PASS: all four specialists called; PASS: this is real multi-agent orchestration not a single agent's fabricated JSON](screenshots/lab-04/multiagent-final-terminal.png)

📚 **Docs:** [Function calling / tools](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/function-calling) · [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) (the recommended long-term path replacing Workflows)

---

## ✅ Checkpoint

**What you built.** An orchestrator that delegates a compound reviewer question to four narrow specialists (Extraction, Screening, Prior-Case, Comms Drafter) and returns one synthesised, evidence-backed reply.

**What CasePal did.**
- Called all four specialists in the trace: Extraction → Screening → Prior-Case → Comms Drafter.
- Assembled a merged JSON reply with the intake, screening findings, prior-case hit, recommendation, and a draft RFI.
- Case ID surfaced as `MDR-2026-0129`; missing document `09-precision` flagged; prior case `MDR-2026-0122` cited; recommendation was `query` (or a synonym); the draft RFI cited SOP-01 §3.2 and asked for CRP precision-and-accuracy data.

**What you learned.**
- **Orchestration is a control pattern, not a model feature.** Four narrow specialists with tight prompts beat one over-instructed agent for complex tasks.
- **Evidence-based decision support ≠ opinion.** The recommendation carries `supporting_evidence` and `rationale`. Without them, it's just a chatbot verdict.
- **Confidence should reflect completeness.** Missing evidence knocks confidence down. If your orchestrator claims 1.0 with `09-precision` missing, tighten the delegation rule.
- **Parallelism is available.** Screening + Prior-Case + Comms Drafter are independent — `lab4_multiagent_concurrent.py` fires them concurrently.

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
