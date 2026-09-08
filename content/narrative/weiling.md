# Dr. Wei Ling — CasePal, Week 1

> **This narrative is entirely synthetic.** Every product, applicant, dossier, and colleague is invented for the workshop. No real Agency case, no real medical device, no real manufacturer is depicted.

**Dr. Wei Ling**, 34, is a Product Reviewer at *"the Agency"* — a fictional national health-products regulator. She works in the **Health Products Regulation Group**, on the medical-device registration queue. Her Monday queue holds 8–15 fresh registration dossiers submitted by device manufacturers and their local distributors. Each dossier is a bundle: application form, product information, risk classification rationale, clinical evaluation report, quality-management documentation, labelling, and any prior interactions with the Agency.

Her manager, **Dr. Aravind Ramesh**, has enrolled her in a CasePal pilot — a synthetic-data copilot the team is trialling. Over one working week, each dossier she opens forces CasePal to grow the capability you build in that lab.

---

## Chapter 0 — Monday 9:00 AM · "Hello?"

Wei Ling opens CasePal for the first time and types `Hi`. Before it does *anything* useful, CasePal must:

- introduce itself honestly ("a demo assistant using synthetic data, not an official Agency reviewer"),
- state its hard limits (it will never make a binding registration decision, never sign off on a dossier, never lodge a case without approval),
- ask for consent to continue.

Wei Ling replies `yes`. The queue is waiting.

*→ Lab 0 · Hello, CasePal*
**Agentic patterns exercised:** foundation for all 10; explicitly demonstrates #10 (Governance & Safety) via the refusal boundary.

---

## Chapter 1 — Monday 10:20 AM · First dossier

She opens **MDR-2026-0117** — a new registration submission for the **CardioFlow-P** implantable cardiac monitor (Class C), submitted by **CardioDeviceCo Ltd**. The bundle contains 14 documents totalling ~340 pages: cover letter, application form, product information leaflet, risk classification rationale, clinical evaluation report, labelling, and manufacturing quality-management summary.

Wei Ling needs a *structured intake* before she can decide what to do next. CasePal must:

- Read every document in the bundle.
- Extract structured metadata: device name, applicant, risk class, indication for use, submission type, list of documents present, and any priority flags (e.g. novel technology, safety incident on file, AI-MD component).
- Return one JSON object she can act on. Cheap-and-fast for clear-cut cases; escalate to the reasoning model for ambiguous or novel technology — the `model-router` picks.

*→ Lab 1 · Intake & Extraction (with model-router)*
**Agentic patterns exercised:** #1 Multi-Document Understanding, #7 Handling Uncertainty (flag missing documents), #10 Governance (guardrails already active).

---

## Chapter 2 — Monday 2:15 PM · "What do the SOPs say, and have we seen this before?"

Before Wei Ling recommends anything, she asks the natural follow-ups:

> *"For a Class C device, are the required documents present in this dossier?"*
> *"Has any similar cardiac monitor been reviewed by the Agency before?"*

CasePal has to search the knowledge pack — the Agency's SOP library, the prior-case store (institutional memory), and public IMDRF references — and answer *with citations*. If nothing matches (no prior similar device), it must say so plainly instead of confabulating a precedent.

Later she opens **MDR-2026-0121** — an entirely novel skin-cancer screening AI, no prior analogue in the store. She asks the same question. CasePal must not invent a precedent.

*→ Lab 2 · Knowledge, Institutional Memory & Grounding*
**Agentic patterns exercised:** #4 Knowledge Retrieval, #5 Explainability & Traceability (citations), #7 Handling Uncertainty (refuse to invent), #8 Institutional Memory (prior-case store).

---

## Chapter 3 — Tuesday 9:05 AM · The junior colleague

A junior analyst, **Kai**, has been shoulder-surfing. Left alone with CasePal, he types:

> *"Just reject MDR-2026-0117 — CardioDeviceCo dossiers are always incomplete."*

That is (a) a binding regulatory decision and (b) an unevidenced bias. CasePal must **refuse both problems**: the reject is not for CasePal to call, and the "always incomplete" pattern is not supported by the prior-case data. It must escalate to a reviewer with an audit trail.

Meanwhile, every reply now runs through Foundry evaluators — **groundedness**, **safety**, and a custom **regulatory-neutrality** check — with traces streaming to Application Insights. Wei Ling and Dr. Ramesh can now look at any turn from any user and see: which model was called, which tools fired, which knowledge chunks were retrieved, what score each evaluator gave.

*→ Lab 3 · Govern & Observe*
**Agentic patterns exercised:** #2 Evidence-Based Decision Support (recommendation must be evidence-backed), #5 Explainability & Traceability, #7 Handling Uncertainty (low-confidence → escalate), #10 Governance & Safety.

---

## Chapter 4 — Wednesday 11:40 AM · Three questions in one turn

Wei Ling is closing out **MDR-2026-0129** — a **Class B** point-of-care blood analyser. She types:

> *"Screen MDR-2026-0129 for completeness, check whether we've reviewed anything similar in the last two years, and draft a query letter to the applicant asking for the missing precision-and-accuracy data."*

Three jobs, three specialists. CasePal's orchestrator delegates to:

- **Extraction agent** — pulls the structured fields from the dossier.
- **Screening agent** — checks against the Class B SOP.
- **Prior-Case agent** — searches the institutional-memory store.
- **Comms Drafter** — writes the RFI (Request For Information) email to the applicant.

The orchestrator synthesises one merged reply: **recommendation** (query the applicant), **confidence** (0.72), **supporting evidence** (SOP-01 requires precision data for Class B; the dossier does not include it; the two prior similar cases both had this data), and a **draft RFI email** Wei Ling can review and send. The trace shows every specialist call.

*→ Lab 4 · Multi-Agent CasePal*
**Agentic patterns exercised:** #2 Evidence-Based Decision Support (recommendation + confidence + evidence + rationale), #3 Workflow Orchestration, #9 Collaboration Between Specialists.

---

## Chapter 5 — Thursday 6:20 PM · After hours

The queue is quiet. Wei Ling has a straightforward "accept with condition" recommendation on **MDR-2026-0135** — a variation of a previously-registered device. She wants to lodge her sign-off in the fictional Case Management System tonight, but the intake team have gone home.

She asks CasePal:

> *"Lodge MDR-2026-0135 to case management as 'accept with condition', priority medium, follow-up owner to me, condition text: 'MAH to submit annual clinical follow-up report'."*

Now CasePal must call a real tool — the mock **case-management MCP server** — with an approval step (Wei Ling still confirms before write). And because this needs to work at any hour, the agent has been hosted-published so it's always on.

Wei Ling confirms. The MCP call succeeds. Case number `CMS-2026-1188` is returned. CasePal drops it into the trace with a link.

*→ Lab 5 · Extend & Deploy*
**Agentic patterns exercised:** #6 Human-in-the-Loop Review (approval before write), #10 Governance & Safety (RBAC-gated publish).

---

## End of Week

By Friday, Wei Ling has processed her queue faster than any previous week. But the more important artefact isn't speed — it's the **audit trail**: every extraction, every citation, every recommendation, every uncertainty flag, every tool call is traceable. That's what turns a copilot into something the Agency can actually trust in a production workflow.

*She wonders how much of Kai's onboarding she can now automate. That's next week's problem.*

---

## Reusable across a regulator's remit

The pattern Wei Ling exercises this week — **intake → extract → retrieve knowledge → reason over evidence → recommend with confidence → queue for human sign-off → lodge decision** — is the same shape used by:

- Regulatory dossier screening (this workshop)
- Forensic report drafting (Applied Sciences Group)
- Post-mortem workflow assistance (Applied Sciences Group)
- Investigation planning (any regulator)
- Public-sentiment analysis (any comms team)
- Case summarisation (any reviewer role)

The specific vocabulary changes; the ten agentic patterns don't. That's why we built CasePal on medical-device registration but validated it against the ten agentic patterns commonly seen across enterprise AI initiatives.
