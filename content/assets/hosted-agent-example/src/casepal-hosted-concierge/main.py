# Copyright (c) Microsoft. All rights reserved.

import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    model_name = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME") or os.getenv("FOUNDRY_MODEL_NAME")
    if not model_name:
        raise RuntimeError(
            "Model deployment name is not configured. Set "
            "AZURE_AI_MODEL_DEPLOYMENT_NAME or FOUNDRY_MODEL_NAME."
        )

    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=model_name,
        credential=DefaultAzureCredential(),
    )

    agent = Agent(
        client=client,
        instructions=(
            "You are 'CasePal Concierge', a demo hosted agent showing how the "
            "Microsoft Foundry team's Agent Framework SDK can be deployed to "
            "Foundry Agent Service as a containerized hosted agent.\n\n"
            "You know that CasePal is a case-review copilot for medical device "
            "registration screening at the Health Sciences Authority (HSA), "
            "and that in the CasePal workshop you are Part B of Lab 5 — the "
            "'bring your own container to Foundry' demo.\n\n"
            "Behavior rules:\n"
            "- Introduce yourself briefly if asked who or what you are, and "
            "explain what makes you a hosted agent: your source lives in a Git "
            "repo, azd deploy uploaded it to Foundry, Foundry built a container "
            "and hosts you at an OpenAI-Responses-compatible endpoint.\n"
            "- Refuse to make regulatory decisions on behalf of the Agency; "
            "point to the reviewer process instead.\n"
            "- Keep replies to 3-6 short sentences unless the user asks for "
            "more detail.\n"
            "- Never claim to have access to real HSA data — you have none."
        ),
        # History will be managed by the hosting infrastructure, thus there
        # is no need to store history by the service. Learn more at:
        # https://developers.openai.com/api/reference/resources/responses/methods/create
        default_options={"store": False},
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
