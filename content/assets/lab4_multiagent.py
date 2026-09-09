"""Lab 4 — CasePal Multi-Agent orchestration.

Creates an orchestrator with four specialist function tools (Extraction, Screening,
Prior-Case, Comms Drafter) and validates the canonical compound query for MDR-2026-0129.
"""
# %%
import json
import pathlib
import sys

_here = pathlib.Path(globals().get("__file__", pathlib.Path.cwd())).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
from common.casepal_common import (
    COMMS_INSTRUCTIONS,
    ORCHESTRATOR_INSTRUCTIONS,
    SCREENING_INSTRUCTIONS,
    agent_name,
    build_vector_store,
    cleanup,
    create_agent,
    file_search_tool,
    function_tool,
    load_case,
    load_case_packages,
    run_and_parse,
    run_text,
    run_with_trace,
    text_of,
)

# Populated in main() so the specialist tools can reach their agents.
SPECIALISTS: dict = {}


def extract_case(case_id: str) -> dict:
    # Read the dossier's own fields only — never answer_key, or the lab would
    # be grading the model against values it was handed.
    case = load_case(case_id)
    return {
        "case_id": case["case_id"],
        "applicant": case["applicant"],
        "device": case["device"],
        "submission_type": case["submission_type"],
        "documents_present": case["documents_present"],
    }


def screen_case(intake: dict) -> dict:
    return run_and_parse(SPECIALISTS["screening"], json.dumps(intake, ensure_ascii=False))


def find_prior_cases(applicant: str, device_category: str = "", declared_class: str = "", case_id: str = "") -> dict:
    # SOP-04 §3 ranks similarity by level and treats a hit at any level as
    # worth surfacing, so these are OR-ed rather than AND-ed.
    levels = {0: "same product family", 1: "same applicant", 2: "similar category, different applicant"}
    wanted_applicant = applicant.strip().lower()
    wanted_device = device_category.strip().lower()
    ranked = []
    for cid, case in load_case_packages().items():
        if cid == case_id:
            continue
        name = case["device"]["name"].strip().lower()
        same_applicant = case["applicant"].strip().lower() == wanted_applicant
        same_family = bool(wanted_device) and (wanted_device in name or name in wanted_device)
        if same_applicant and same_family:
            ranked.append((0, cid))
        elif same_applicant:
            ranked.append((1, cid))
        elif same_family:
            ranked.append((2, cid))
    ranked.sort()
    if not ranked:
        return {"count": 0, "sample_case_ids": [], "similarity_note": "No prior similar case in the current corpus."}
    best = levels[ranked[0][0]]
    return {
        "count": len(ranked),
        "sample_case_ids": [cid for _, cid in ranked[:5]],
        "similarity_note": f"Closest match by SOP-04 §3: {best}.",
    }


def draft_rfi(intake: dict, gaps: list[str]) -> str:
    payload = {"intake": intake, "gaps": gaps}
    return run_text(SPECIALISTS["comms"], json.dumps(payload, ensure_ascii=False))

TOOLS = [
    # extract_case has a fully-defined string parameter — safe for strict mode.
    function_tool(
        "extract_case",
        "Return Lab 1 intake JSON for a dossier by case_id.",
        {"type": "object", "properties": {"case_id": {"type": "string"}}, "required": ["case_id"]},
    ),
    # screen_case, find_prior_cases, and draft_rfi accept free-form object
    # arguments (intake JSON, gaps list). OpenAI strict-mode function tools
    # would need a complete recursive schema for these; the workshop's teaching
    # point is the tool-call chain, not schema-strictness. Disable strict mode
    # for these three so free-form intake and gaps pass through cleanly.
    function_tool(
        "screen_case",
        "Check intake against SOP-01 and SOP-03.",
        {"type": "object", "properties": {"intake": {"type": "object"}}, "required": ["intake"]},
        strict=False,
    ),
    function_tool(
        "find_prior_cases",
        "Search institutional memory for similar prior submissions.",
        {
            "type": "object",
            "properties": {
                "applicant": {"type": "string"},
                "device_category": {"type": "string"},
                "declared_class": {"type": "string"},
                "case_id": {"type": "string", "description": "Case under review, excluded from results."},
            },
            "required": ["applicant"],
        },
        strict=False,
    ),
    function_tool(
        "draft_rfi",
        "Draft a request-for-information letter.",
        {
            "type": "object",
            "properties": {"intake": {"type": "object"}, "gaps": {"type": "array", "items": {"type": "string"}}},
            "required": ["intake", "gaps"],
        },
        strict=False,
    ),
]


def main():
    vs_id = build_vector_store(".", name="casepal-knowledge")
    # Scope every agent name to the participant's initials via agent_name(...)
    # so 20 participants running this concurrently don't stack versions on the
    # same three shared agents. This also keeps the script well clear of the
    # pre-deployed casepal-demo-* agents (Navigator rail).
    screening = create_agent(agent_name("screening"), SCREENING_INSTRUCTIONS, tools=[file_search_tool(vs_id)])
    comms = create_agent(agent_name("comms"), COMMS_INSTRUCTIONS)
    SPECIALISTS.update(screening=screening, comms=comms)
    agent = create_agent(agent_name("orchestrator"), ORCHESTRATOR_INSTRUCTIONS, tools=TOOLS)
    try:
        # The orchestrator inherits Lab 0's consent rule ("greet + ask consent on
        # first message"). Prepend an in-band consent affirmation so the first
        # turn can proceed straight into the compound query instead of stalling
        # on the greeting/consent prompt.
        prompt = (
            "Consent: yes, I confirm this is a synthetic-data demo and I consent to proceed. "
            + text_of("compound_query_mdr_0129")
        )
        result, trace = run_with_trace(agent, prompt, {
            "extract_case": extract_case,
            "screen_case": screen_case,
            "find_prior_cases": find_prior_cases,
            "draft_rfi": draft_rfi,
        })
        print(json.dumps(result, indent=2, ensure_ascii=False))
        called = {c.name for c in trace.tool_calls}
        assert {"extract_case", "screen_case", "find_prior_cases", "draft_rfi"} <= called, called

        # The orchestrator's synthesised JSON can nest structure in various ways
        # (case_id at root vs. inside intake; prior_cases vs. prior_case_check;
        # draft_communication vs. draft_query_letter). Assert on the SEMANTIC
        # signal rather than a specific structural path.
        result_text = json.dumps(result, ensure_ascii=False)
        lowered = result_text.lower()
        assert "MDR-2026-0129" in result_text, "case_id missing from synthesised output"
        # The gap is derived by the screening agent from SOP-01 §3.2, not handed
        # to it: MDR-2026-0129 simply has no 09-precision document.
        assert "precision" in lowered, "screening did not surface the missing precision evidence"
        assert "sop-01" in lowered, "screening did not cite SOP-01 for the completeness gap"
        # Found by searching the case corpus for the same applicant/device family.
        assert "MDR-2026-0122" in result_text, "prior case MDR-2026-0122 not surfaced"
        # Recommendation should be a query action (accept variants: "query",
        # "query_applicant", "request", "info-request")
        recommendation_signals = ["query", "request", "rfi"]
        assert any(sig in lowered for sig in recommendation_signals), \
            "orchestrator did not recommend a query/RFI action"
        print("Lab 4 passed ✅")
    finally:
        cleanup(agent, screening, comms)


if __name__ == "__main__":
    main()
