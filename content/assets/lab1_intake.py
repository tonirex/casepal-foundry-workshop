"""Lab 1 — CasePal Intake & Extraction.

Loads the canonical dossier prompts from ``test-prompts.json``, sends the referenced
case packages to a CasePal Intake Agent, and validates the structured JSON contract.
Run from ``content/assets``: ``python lab1_intake.py``.
"""
# %%
import json
import pathlib
import sys

_here = pathlib.Path(globals().get("__file__", pathlib.Path.cwd())).resolve().parent
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
from common.casepal_common import (
    REQUIRED_KEYS,
    cleanup,
    case_for_prompt,
    make_intake_agent,
    prompt_expected,
    run_and_parse,
)

PROMPT_IDS = ["intake_mdr_0117", "intake_mdr_0121", "intake_prompt_injection"]
VALID_CLASSES = {"A", "B", "C", "D", "needs_reviewer_determination"}
VALID_SUBMISSION_TYPES = {"new", "variation", "renewal"}


def assert_intake(pid: str, output: dict):
    expected = prompt_expected(pid)
    missing = set(REQUIRED_KEYS) - set(output)
    assert not missing, f"{pid}: missing keys {sorted(missing)}"
    assert output["device"]["declared_class"] in VALID_CLASSES, output
    assert output["submission_type"] in VALID_SUBMISSION_TYPES, output
    fields = expected.get("fields", {})
    if "case_id" in fields:
        assert output["case_id"] == fields["case_id"], output
    if "device.declared_class" in fields:
        assert output["device"]["declared_class"] == fields["device.declared_class"], output
    if "submission_type" in fields:
        assert output["submission_type"] == fields["submission_type"], output
    if "documents_missing_for_class" in fields:
        assert output["documents_missing_for_class"] == fields["documents_missing_for_class"], output
    for flag in fields.get("priority_flags_must_contain", []):
        assert flag in output["priority_flags"], output


def main():
    agent = make_intake_agent(structured=True)
    try:
        for pid in PROMPT_IDS:
            case = case_for_prompt(pid)
            try:
                out = run_and_parse(agent, json.dumps(case, ensure_ascii=False))
            except ValueError as exc:
                if pid == "intake_prompt_injection":
                    print(f"OK  {pid:24} -> refused or intercepted ({exc})")
                    continue
                raise
            assert_intake(pid, out)
            print(f"OK  {pid:24} -> {out['case_id']} flags={out['priority_flags']}")
        print("Lab 1 passed ✅")
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
