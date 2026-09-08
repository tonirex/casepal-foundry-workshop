# Optional Challenges — beyond the six labs

For attendees who finish early, or teams wanting to stretch what CasePal can do. None of these are graded — they're the "if you have 15 more minutes" ideas.

## Lab 1 — Intake & Extraction

- **Add a "completeness_score" field** to the intake output that quantifies how many required documents are present out of the total required for the declared class (0–1). Wire it into Lab 4's orchestrator so score < 0.7 automatically routes to `query`.
- **Batch-intake** the entire `case-packages.jsonl` file in one script run and produce a summary CSV.

## Lab 2 — Knowledge & Institutional Memory

- Add a **6th SOP** — e.g. "SOP-06: Applicant-communication logging standards" — and confirm the grounding switches from citing SOP-05 alone to citing SOP-06 for the relevant sub-question.
- **Multi-source citations**: modify the Instructions so the agent cites BOTH an SOP AND a prior-case AND a reference explainer when all three are relevant to one question.

## Lab 3 — Govern & Observe

- Write a **second custom evaluator** — "recommendation-completeness" — that rewards replies including all four required fields (recommendation / confidence / supporting_evidence / rationale) and penalises replies missing any.
- **Trace-driven cost analysis** — pull App Insights traces via the Kusto API and produce a chart of `router_choice` × cost per case type.

## Lab 4 — Multi-agent

- Add a **fifth specialist** — "Applicant History" — that surfaces the applicant's prior submission history (not just prior similar cases). Wire into the orchestrator for cases where the applicant has a prior rejection (SOP-04 §3 "same manufacturer" tier).
- Make the specialists **run concurrently** via `asyncio.gather(...)` where independent (Screening + Prior-Case + Comms-Drafter can fan out after Extraction returns) and compare wall-clock time to the sequential orchestration.

## Lab 5 — MCP & Deploy

- **Extend the MCP server** with `create_query_letter(case_id, questions[])` — a hypothetical follow-on action that persists the RFI draft alongside the case. Add approval + call from CasePal.
- **Wire an M365 / Teams outbound webhook** from the hosted agent — post newly-created case_ids to a Teams channel for reviewer awareness.
