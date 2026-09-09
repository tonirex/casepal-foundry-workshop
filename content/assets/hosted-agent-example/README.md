# Foundry hosted agent example — Lab 5, Part B

This is the exact scaffold the facilitator deployed for the workshop's Part B walkthrough. It is an adapted copy of the [Basic Agent Framework hosted-agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/01-basic), with:

- Rebranded as **CasePal Concierge** via the `main.py` Instructions block
- Deployed **into the `casepal-workshop` Foundry project** so it sits alongside the other CasePal agents — no separate resource group, no separate account

## Live deployment

| Field | Value |
|---|---|
| Foundry account | `aif-casepal-workshop-sc` (Sweden Central) |
| Foundry project | `casepal-workshop` |
| Hosted agent name | `casepal-hosted-concierge` (v1) |
| Runtime | `python_3_13` · Agent Framework `ResponsesHostServer` |
| Model deployment | `gpt-5-mini` (existing GlobalStandard deployment, 300 TPM) |
| CPU / Memory | 0.5 vCPU / 1 GiB |
| Portal playground | [ai.azure.com → casepal-hosted-concierge v1](https://ai.azure.com/nextgen/r/xHRanC-2QzagAG4Pca-utQ,rg-casepal-workshop,,aif-casepal-workshop-sc,casepal-workshop/build/agents/casepal-hosted-concierge/build?version=1) |
| Responses endpoint | `https://aif-casepal-workshop-sc.services.ai.azure.com/api/projects/casepal-workshop/agents/casepal-hosted-concierge/endpoint/protocols/openai/responses?api-version=v1` |
| Resource group | `rg-casepal-workshop` (same as all other CasePal resources) |

Look for it at the bottom of the **Agents** list in the CasePal portal — right next to `casepal-demo-*`.

## What the sample actually does

`src/casepal-hosted-concierge/main.py`:

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

The scaffold is pre-configured to deploy into the **existing** `casepal-workshop` project — no new provisioning needed.

```powershell
# From this folder (content/assets/hosted-agent-example/)
azd ext install microsoft.foundry     # first time only
azd auth login --tenant-id <tenant-id>

azd env new casepal-hosted-dev
azd env set AZURE_SUBSCRIPTION_ID <sub-id>
azd env set AZURE_LOCATION swedencentral
azd env set AZURE_RESOURCE_GROUP rg-casepal-workshop
azd env set USE_EXISTING_AI_PROJECT true
azd env set AZURE_AI_PROJECT_ID "/subscriptions/<sub-id>/resourceGroups/rg-casepal-workshop/providers/Microsoft.CognitiveServices/accounts/aif-casepal-workshop-sc/projects/casepal-workshop"
azd env set AZURE_AI_PROJECT_NAME casepal-workshop
azd env set FOUNDRY_PROJECT_ENDPOINT "https://aif-casepal-workshop-sc.services.ai.azure.com/api/projects/casepal-workshop"
azd env set AZURE_AI_PROJECT_CONNECTIONS_PROJECT_ENDPOINT "https://aif-casepal-workshop-sc.services.ai.azure.com/api/projects/casepal-workshop"
azd env set AZURE_OPENAI_ENDPOINT "https://aif-casepal-workshop-sc.openai.azure.com/"
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME gpt-5-mini

azd deploy      # ~2 min — packages code, uploads to Foundry, waits for container to warm
azd ai agent invoke casepal-hosted-concierge "Who are you?"
```

## Clean up

```powershell
# Delete just the hosted agent (leaves the CasePal project standing)
azd ai agent delete casepal-hosted-concierge
```

Because we're using an existing Foundry project (`USE_EXISTING_AI_PROJECT=true`), `azd down` **won't** delete the whole resource group — it only removes the hosted agent version.
