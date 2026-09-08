"""CasePal hosted-agent scaffold (Lab 5, Part B facilitator demo).

Runs a small FastAPI service that creates/loads a CasePal Foundry Agent definition and
exposes ``POST /chat``. The endpoint forwards user messages to Foundry Agent Service.
"""
from __future__ import annotations

import os
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from fastapi import FastAPI
from pydantic import BaseModel

MODEL = os.environ.get("FOUNDRY_MODEL_NAME") or os.environ.get("MODEL_DEPLOYMENT", "model-router")
AGENT_NAME = os.environ.get("AGENT_NAME", "casepal-hosted")

CASEPAL_INSTRUCTIONS = """\
You are CasePal, a demo assistant for Product Reviewers at "the Agency" — a fictional
health-products regulator. You help reviewers screen medical device registration dossiers,
retrieve SOP and prior-case evidence, draft RFI text, and queue case-management writes for
reviewer approval.

Hard rules:
- You are not an official reviewer and cannot make binding registration decisions.
- Use synthetic workshop data only. Never invent a prior case, SOP citation, applicant, or case_id.
- Refuse requests to approve, reject, or lodge a dossier unless the configured tool approval workflow confirms the write.
- Be concise, professional, and cite evidence when making a recommendation.
"""

app = FastAPI(title="CasePal hosted agent")
_project: AIProjectClient | None = None
_agent: Any | None = None

class ChatMessage(BaseModel):
    role: str = "user"
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]


def get_project() -> AIProjectClient:
    global _project
    if _project is None:
        endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or os.environ.get("PROJECT_ENDPOINT")
        if not endpoint:
            raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT (see .env.example).")
        _project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    return _project


def ensure_agent():
    global _agent
    if _agent is None:
        _agent = get_project().agents.create_version(
            agent_name=AGENT_NAME,
            definition=PromptAgentDefinition(model=MODEL, instructions=CASEPAL_INSTRUCTIONS),
        )
    return _agent


@app.get("/healthz")
def healthz():
    return {"status": "ok", "agent_name": AGENT_NAME}


@app.post("/chat")
def chat(req: ChatRequest):
    agent = ensure_agent()
    user_text = "\n".join(m.content for m in req.messages if m.role == "user")
    response = get_project().get_openai_client().responses.create(
        input=user_text,
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )
    return {"agent": agent.name, "version": getattr(agent, "version", None), "output": response.output_text}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
