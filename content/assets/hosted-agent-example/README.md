# Foundry hosted agent example — Lab 5, Part B

This is the exact scaffold the facilitator deployed for tomorrow's Part B walkthrough. It is a copy of the [Basic Agent Framework hosted-agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/01-basic) with the agent's Instructions rebranded as "CasePal Concierge".

## Live deployment

| Field | Value |
|---|---|
| Foundry project | `agent-framework-agent-basic-resp` (Sweden Central) |
| Hosted agent name | `agent-framework-agent-basic-responses` (v3) |
| Runtime | `python_3_13` · Agent Framework `ResponsesHostServer` |
| Model deployment | `gpt-5.4-mini` (GlobalStandard, 10 TPM) |
| CPU / Memory | 0.5 vCPU / 1 GiB |
| Portal playground | [ai.azure.com — hosted agent](https://ai.azure.com/nextgen/r/xHRanC-2QzagAG4Pca-utQ,rg-agent-framework-agent-basic-responses-dev-516d423c,,cog-gsftpeygf77pu,agent-framework-agent-basic-resp/build/agents/agent-framework-agent-basic-responses/build?version=3) |
| Responses endpoint | `https://cog-gsftpeygf77pu.services.ai.azure.com/api/projects/agent-framework-agent-basic-resp/agents/agent-framework-agent-basic-responses/endpoint/protocols/openai/responses?api-version=v1` |

The agent is deliberately in a **different Foundry project** from the main workshop (`casepal-workshop`) — it's a separate resource group (`rg-agent-framework-agent-basic-responses-dev-516d423c`) so that the "bring-your-own-container" story stays cleanly separable and doesn't tangle with the CasePal agent set.

## What the sample actually does

`src/agent-framework-agent-basic-responses/main.py`:

```python
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    credential=DefaultAzureCredential(),
)

agent = Agent(
    client=client,
    instructions="You are 'CasePal Concierge' ...",  # CasePal-branded instructions
    default_options={"store": False},
)

server = ResponsesHostServer(agent)
server.run()   # exposes an OpenAI-Responses-compatible HTTP endpoint on 0.0.0.0:8088
```

`azure.yaml` tells Foundry how to build and host it — Python 3.13 runtime, entry point `main.py`, 0.5 CPU / 1 GiB, `responses` protocol version 2.0.0.

## How to redeploy or extend this

```powershell
# From this folder (content/assets/hosted-agent-example/)
azd ext install microsoft.foundry     # first time only
azd auth login --tenant-id <tenant-id>

azd env set AZURE_SUBSCRIPTION_ID <sub-id>
azd env set AZURE_LOCATION swedencentral
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME gpt-5.4-mini

azd provision   # ~2 min — creates RG, Foundry account, gpt-5.4-mini deployment
azd deploy      # ~1-2 min — packages code, uploads to Foundry, waits for container to warm
azd ai agent invoke "Who are you?"
```

## Clean up

```powershell
azd down   # deletes the RG + Foundry project + hosted agent
```

> `azd down` **permanently deletes the resource group** because azd created it. If you point this scaffold at an existing Foundry project instead (via `USE_EXISTING_AI_PROJECT=true`), `azd down` only removes the hosted agent version and leaves the project standing.
