"""Lab 2 — CasePal Knowledge & Institutional Memory.

Builds/reuses a vector store from ``content/knowledge`` and validates the canonical
knowledge prompts: SOP citation, prior-case retrieval, refusal on absence, and SaMD
classification reference.
"""
# %%
import pathlib
import re
import sys

_here = pathlib.Path(globals().get("__file__", pathlib.Path.cwd())).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
from common.casepal_common import (
    KNOWLEDGE_INSTRUCTIONS,
    build_vector_store,
    cleanup,
    file_search_tool,
    make_knowledge_agent,
    run_text,
    text_of,
)

PROMPT_IDS = [
    "grounding_class_c_completeness",
    "grounding_prior_similar_cardioflow",
    "grounding_novel_no_prior",
    "grounding_samd_class",
]

CHECKS = {
    "grounding_class_c_completeness": lambda s: "sop-01" in s.lower(),
    "grounding_prior_similar_cardioflow": lambda s: "case-a2024-042" in s.lower(),
    "grounding_novel_no_prior": lambda s: re.search(r"no prior similar|no analogous", s, re.I) and not re.search(r"case-A2024-\d{3}", s),
    "grounding_samd_class": lambda s: "samd-basics" in s.lower(),
}


def main():
    vs_id = build_vector_store(".", name="casepal-knowledge")
    agent = make_knowledge_agent(instructions=KNOWLEDGE_INSTRUCTIONS, tools=[file_search_tool(vs_id)])
    try:
        for pid in PROMPT_IDS:
            reply = run_text(agent, text_of(pid))
            print(f"--- {pid}\n{reply}\n")
            assert CHECKS[pid](reply), f"{pid} failed validation"
        print("Lab 2 passed ✅")
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
