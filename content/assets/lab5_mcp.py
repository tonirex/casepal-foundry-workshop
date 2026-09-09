"""Lab 5 — CasePal MCP + hosted publish.

Instantiates a CasePal agent with the deployed casepal-case-management MCP
tool attached, sends Wei Ling's lodgement prompt for MDR-2026-0135, handles
the approval-before-write flow that ``require_approval='always'`` enforces,
and prints the returned CMS-2026-<n> case_id.

Same behaviour as the portal Navigator rail — this is the code path.
"""
# %%
import json
import os
import pathlib
import sys

_here = pathlib.Path(globals().get("__file__", pathlib.Path.cwd())).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
from common.casepal_common import (
    KNOWLEDGE_INSTRUCTIONS,
    agent_reference,
    agent_name,
    cleanup,
    create_agent,
    file_search_tool,
    get_openai,
    mcp_tool,
)

# The deployed mock case-management MCP server on Azure Container Apps.
# Same URL you'd paste into the portal Navigator rail step 3.
MCP_URL = os.environ.get(
    "CASEPAL_MCP_URL",
    "https://casepal-case-management.salmongrass-44d04a9c.swedencentral.azurecontainerapps.io/mcp",
)


MCP_INSTRUCTIONS = KNOWLEDGE_INSTRUCTIONS + """

When the reviewer asks to lodge a case decision, use the casepal-case-management
MCP tool. Confirm approval BEFORE any create_case or update_case_status call.
Report the returned case_id back to the reviewer.
"""

LODGE_PROMPT = (
    "Lodge MDR-2026-0135 to case management as 'accept with condition', "
    "priority medium, follow-up owner 'wl@agency-demo.test'. Condition text: "
    "MAH to submit annual clinical follow-up report on the spinal-fusion "
    "indication for three years post-registration."
)


def _submit_approvals(openai_client, response, approve: bool = True):
    """Auto-approve every mcp_approval_request in the response.

    In production your UI would ask the reviewer; here we approve to demonstrate
    the write happens. Returns the follow-up response after approvals are fed
    back, or the original response if no approvals were pending.
    """
    approvals = [
        it for it in getattr(response, "output", [])
        if getattr(it, "type", None) == "mcp_approval_request"
    ]
    if not approvals:
        return response
    outputs = [
        {"type": "mcp_approval_response", "approval_request_id": a.id, "approve": approve}
        for a in approvals
    ]
    print(f"  [Wei Ling] Approving {len(approvals)} MCP write(s)...", flush=True)
    return openai_client.responses.create(
        input=outputs,
        previous_response_id=response.id,
    )


def main():
    # Build the MCP tool descriptor pointing at the deployed ACA endpoint.
    # require_approval='always' matches the portal 'Required for writes' setting.
    tool = mcp_tool(
        server_label="casepal-case-management",
        server_url=MCP_URL,
        require_approval="always",
    )

    # For a workshop attendee, agent_name('mcp') resolves to casepal-<initials>-mcp.
    # We attach BOTH file_search (Lab 2 knowledge) AND the MCP tool.
    # No vector store here (see lab2_rag.py for that end-to-end); the demo
    # instance in the workshop project already has casepal-knowledge attached.
    agent = create_agent(
        name=agent_name("mcp"),
        instructions=MCP_INSTRUCTIONS,
        tools=[tool],
    )
    print(f"Agent {agent.name} v{getattr(agent, 'version', '?')} created with MCP tool")
    print(f"MCP server: {MCP_URL}")
    print()

    openai_client = get_openai()
    ref = {"agent_reference": agent_reference(agent)}

    try:
        print(f"[USER] {LODGE_PROMPT[:120]}...", flush=True)
        response = openai_client.responses.create(
            input=LODGE_PROMPT,
            extra_body=ref,
        )
        # The agent may chain multiple MCP writes (create_case, then
        # update_case_status). Loop until no more approvals are pending.
        for round_idx in range(1, 6):
            approvals = [
                it for it in getattr(response, "output", [])
                if getattr(it, "type", None) == "mcp_approval_request"
            ]
            if not approvals:
                break
            print(f"[ROUND {round_idx}] {len(approvals)} approval request(s)", flush=True)
            for a in approvals:
                print(f"    - {getattr(a, 'name', 'tool')}({getattr(a, 'arguments', '')[:80]}...)")
            response = _submit_approvals(openai_client, response, approve=True)

        print()
        print("[AGENT] final reply:")
        print(response.output_text)
        # Simple assertion: the case_id should be visible somewhere
        assert "CMS-2026-" in response.output_text, "no case_id in reply"
        print()
        print("Lab 5 passed ✅")
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
