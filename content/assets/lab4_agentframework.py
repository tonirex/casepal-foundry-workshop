"""Lab 4 (variant) — CasePal orchestration via Microsoft Agent Framework workflows.

Same case as ``lab4_multiagent.py``, but the specialists are composed with the
Agent Framework's built-in orchestration patterns instead of a single orchestrator
agent driving function tools:

    Extraction (data)  ->  ConcurrentBuilder[Screening || Prior-Case]  ->  Comms Drafter

Docs: https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/
"""
# %%
import asyncio
import json
import os
import pathlib
import sys

_here = pathlib.Path(globals().get("__file__", pathlib.Path.cwd())).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
from azure.identity.aio import DefaultAzureCredential
from agent_framework_foundry import FoundryChatClient
from agent_framework_orchestrations import ConcurrentBuilder

from common.casepal_common import (
    COMMS_INSTRUCTIONS,
    MODEL,
    PRIOR_CASE_INSTRUCTIONS,
    SCREENING_INSTRUCTIONS,
    build_vector_store,
)
from lab4_multiagent import extract_case, find_prior_cases


def _participant_texts(result) -> list[str]:
    # Outputs without a response_id are the aggregated conversation the workflow
    # emits alongside the participants, not a specialist reply.
    return [
        response.text
        for response in result.get_outputs()
        if getattr(response, "response_id", None) and (response.text or "").strip()
    ]


async def main():
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or os.environ["PROJECT_ENDPOINT"]
    vs_id = build_vector_store(".", name="casepal-knowledge")
    intake = extract_case("MDR-2026-0129")

    async with DefaultAzureCredential() as credential:
        client = FoundryChatClient(project_endpoint=endpoint, model=MODEL, credential=credential)

        screening = client.as_agent(
            name="screening",
            instructions=SCREENING_INSTRUCTIONS,
            tools=client.get_file_search_tool(vector_store_ids=[vs_id]),
        )
        # Agent Framework builds the tool schema from the function signature.
        prior_case = client.as_agent(
            name="prior_case",
            instructions=PRIOR_CASE_INSTRUCTIONS,
            tools=find_prior_cases,
        )
        comms = client.as_agent(name="comms", instructions=COMMS_INSTRUCTIONS)

        # output_from="all": without it the workflow yields only one participant's
        # result, so the other specialist's findings would be silently dropped.
        fan_out = ConcurrentBuilder(participants=[screening, prior_case], output_from="all").build()
        specialist_result = await fan_out.run(json.dumps(intake, ensure_ascii=False))
        findings = _participant_texts(specialist_result)
        assert len(findings) == 2, f"expected both specialists to reply, got {len(findings)}"
        for text in findings:
            print(f"--- specialist ---\n{text[:400]}\n")

        draft = await comms.run(json.dumps({"intake": intake, "findings": findings}, ensure_ascii=False))
        print(f"--- comms draft ---\n{draft.text[:400]}\n")

        blob = " ".join(findings).lower()
        assert "precision" in blob, "screening did not derive the missing precision evidence"
        assert "sop-01" in blob, "screening did not cite SOP-01"
        assert "MDR-2026-0122" in " ".join(findings), "prior-case specialist did not surface MDR-2026-0122"
        assert draft.text.strip(), "comms drafter returned no RFI"
        print("Lab 4 (Agent Framework variant) passed ✅")


if __name__ == "__main__":
    asyncio.run(main())
