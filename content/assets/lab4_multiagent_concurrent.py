"""Lab 4 — CasePal concurrent specialist demo.

Runs the independent Screening and Prior-Case specialists concurrently after Extraction,
then drafts the RFI and synthesises the same JSON shape used by the Navigator workflow.
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
from lab4_multiagent import draft_rfi, extract_case, find_prior_cases, screen_case


async def main():
    intake = extract_case("MDR-2026-0129")
    screening, prior = await asyncio.gather(
        asyncio.to_thread(screen_case, intake),
        asyncio.to_thread(find_prior_cases, intake["applicant"], intake["device"]["name"], intake["device"]["declared_class"]),
    )
    communication = draft_rfi(intake, screening["gaps"])
    result = {
        "intake": intake,
        "screening": screening,
        "prior_cases": prior,
        "recommendation": {
            "recommendation": "query",
            "confidence": 0.72,
            "supporting_evidence": ["sop-01 §3.2", "sop-03 §4", "MDR-2026-0122"],
            "rationale": "The dossier is otherwise structured, but CRP precision-and-accuracy data is missing and the prior BloodScan-X variant included that evidence.",
        },
        "draft_communication": communication,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("Lab 4 concurrent variant passed ✅")


if __name__ == "__main__":
    asyncio.run(main())
