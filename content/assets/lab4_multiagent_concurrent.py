"""Lab 4 — CasePal concurrent specialist demo.

Runs the independent Screening and Prior-Case specialists concurrently after Extraction,
then drafts the RFI. For the same fan-out expressed with the Microsoft Agent Framework's
built-in orchestration patterns, see ``lab4_agentframework.py``.
"""
# %%
import asyncio
import json
import pathlib
import sys

_here = pathlib.Path(globals().get("__file__", pathlib.Path.cwd())).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
from common.casepal_common import (
    COMMS_INSTRUCTIONS,
    SCREENING_INSTRUCTIONS,
    agent_name,
    build_vector_store,
    cleanup,
    create_agent,
    file_search_tool,
)
from lab4_multiagent import SPECIALISTS, draft_rfi, extract_case, find_prior_cases, screen_case


async def main():
    vs_id = build_vector_store(".", name="casepal-knowledge")
    # Same participant-scoping rule as lab4_multiagent.py — see notes there.
    screening = create_agent(agent_name("screening"), SCREENING_INSTRUCTIONS, tools=[file_search_tool(vs_id)])
    comms = create_agent(agent_name("comms"), COMMS_INSTRUCTIONS)
    SPECIALISTS.update(screening=screening, comms=comms)
    try:
        intake = extract_case("MDR-2026-0129")
        screening_result, prior = await asyncio.gather(
            asyncio.to_thread(screen_case, intake),
            asyncio.to_thread(
                find_prior_cases,
                intake["applicant"],
                intake["device"]["name"],
                intake["device"]["declared_class"],
                intake["case_id"],
            ),
        )
        gaps = screening_result["gaps"]
        communication = draft_rfi(intake, gaps)
        result = {
            "intake": intake,
            "screening": screening_result,
            "prior_cases": prior,
            # SOP-01 §4: an absent required document is queried, never rejected.
            "recommendation": {
                "recommendation": "query" if gaps else "proceed_to_reviewer",
                "supporting_evidence": screening_result.get("sop_citations", []) + prior["sample_case_ids"],
                "rationale": "; ".join(gaps) if gaps else "No completeness gaps found against the declared class.",
            },
            "draft_communication": communication,
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
        assert gaps, "screening returned no gaps for a dossier missing precision data"
        assert any("precision" in gap.lower() for gap in gaps), gaps
        assert prior["sample_case_ids"] == ["MDR-2026-0122"], prior
        assert communication.strip(), "comms drafter returned no RFI"
        print("Lab 4 concurrent variant passed ✅")
    finally:
        cleanup(screening, comms)


if __name__ == "__main__":
    asyncio.run(main())
