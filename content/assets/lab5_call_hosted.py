"""Lab 5, Part B — call a Foundry-hosted agent from an external process.

Point: every agent created with PromptAgentDefinition in Foundry is already
Foundry-hosted. There's no separate "publish" step, no App Service, no ACA.
The Responses API + agent_reference is the hosted endpoint.

This script is the facilitator demo for Part B: it calls
`casepal-demo-hosted-mcp` (the MCP-enabled agent you configured in Part A)
from a plain Python process, gets a real case_id from the case-management
MCP tool, and shows that the tool + approval + evaluators all come along
for free.

Run:
    az login
    pip install azure-ai-projects azure-identity openai
    python lab5_call_hosted.py
"""
from __future__ import annotations

import os
import time

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

ENDPOINT = os.environ.get(
    "FOUNDRY_PROJECT_ENDPOINT",
    "https://aif-casepal-workshop-sc.services.ai.azure.com/api/projects/casepal-workshop",
)
AGENT_NAME = os.environ.get("AGENT_NAME", "casepal-demo-hosted-mcp")

PROMPT = (
    "Lodge MDR-2026-0135 to case management as 'accept with condition', "
    "priority medium, follow-up owner 'wl@agency-demo.test'. Condition text: "
    "MAH to submit annual clinical follow-up report on the spinal-fusion "
    "indication for three years post-registration."
)


def main() -> None:
    project = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    openai = project.get_openai_client()

    print(f"-> Calling Foundry-hosted agent {AGENT_NAME!r}")
    print(f"  Endpoint (project):  {ENDPOINT}")
    print(f"  Auth:                DefaultAzureCredential (Entra ID)")
    print(f"  Client rides on:     openai.responses.create() + agent_reference")
    print()

    t0 = time.time()
    resp = openai.responses.create(
        input=PROMPT,
        extra_body={
            "agent_reference": {
                "name": AGENT_NAME,
                "type": "agent_reference",
            }
        },
    )
    elapsed = time.time() - t0

    print(f"<- Response in {elapsed:.1f}s")
    print(f"  Response ID:         {resp.id}")
    print(f"  Total tokens:        {resp.usage.total_tokens}")
    print()
    print("--- Agent output --------------------------------------------")
    print(resp.output_text)
    print("-------------------------------------------------------------")
    print()
    print("Note: the case_id above was created via the case-management MCP")
    print("tool wired into casepal-demo-hosted-mcp — same tool, same store")
    print("as the Portal Playground you used in Part A.")


if __name__ == "__main__":
    main()
