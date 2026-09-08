# CasePal Foundry Day — workshop content

Loadable content for *An enterprise Case Review Copilot, built on Microsoft Foundry*. Authored from
`../foundry-workshop-plan.md`.

```
content/
  config/workshop.yaml                        # platform config (shared project, rails, labs)
  admin/ADMIN-SETUP.md                        # admin & pre-workshop logistics (RBAC script, models, MCP)
  narrative/weiling.md                        # reviewer story — one chapter per lab
  prompts/test-prompts.json                   # SINGLE SOURCE OF TRUTH for canned prompts + expected outputs
  labs/lab-00.md ... lab-05.md                # participant-facing, rail-tabbed (Navigator / Builder)
  answer-keys/lab-00.json ... lab-05.json     # SERVER-SIDE ONLY validators (never ship to client)
  knowledge/                                  # RAG source for Lab 2 (and reused by Lab 4)
    README.md                                 #   knowledge pack map + ground-truth answers
    sop-library/                              #   5 synthetic Agency SOPs
    prior-cases/                              #   5 completed prior-case decisions (institutional memory)
    references/                               #   IMDRF / clinical-eval / dossier-structure / SaMD / links
    fake-registry.md                          #   fake product & applicant registry + collision policy
  assets/                                     # runnable starter code
    common/casepal_common.py                  #   one helper that talks to Foundry Agent Service
    lab1_intake.* ... lab4_multiagent.*       #   notebook (canonical) + auto-derived script
    mcp-case-management/                      #   Lab 5 Part A — mock case-management MCP server
    hosted-deploy/                            #   Lab 5 Part B — hosted-agent deploy scaffold
    case-packages.jsonl                       #   15 synthetic device dossiers used across labs
    casepal-eval-dataset.{csv,jsonl}          #   Lab 3 evaluation dataset
```

## How the pieces fit

- **Each lab** exercises at least two of the ten agentic patterns explicitly named in the root README.
- **Each lab** states one shared **objective** + **validation checkpoint**, then two **rails** to get there.
- **Validators** live in `answer-keys/` and reference `prompts/test-prompts.json` by `prompt_id`.
- **Enums** are defined once in `answer-keys/_schema.json` and `prompts/test-prompts.json` — keep them in sync.
- **Knowledge ground truths** are enumerated in `knowledge/README.md` so Lab 2 answer keys can be validated
  automatically.

## Two rails only

The earlier three-rail split collapsed to two for CasePal:
- 🟢 **Navigator** — no-code, Foundry portal. For CIOs, IT leaders, and non-coding attendees.
- 🔵 **Builder** — canonical Jupyter notebooks. `.py` scripts are auto-derived via `jupyter nbconvert`
  and shipped as a convenience for SIs who prefer scripts, but they are *not* hand-maintained separately.

## Security

- `answer-keys/*.json` load **only** inside server-side validator code. Never import in client
  components, return in API responses, or place under a public path.
- Run any validator script (must exit 0) before go-live.

## Synthetic-data guarantee

Every product name, applicant, dossier, MAH, and case ID is invented. See
[`knowledge/fake-registry.md`](knowledge/fake-registry.md).

## Status

**Draft** — reskinned from an earlier workshop and further broadened from a pharmacovigilance
scenario to a generic case-review scenario. Content substitution complete; per-lab troubleshooting KB,
portal walkthroughs (`lab-0N-portal.md`), and end-to-end live-run against a Foundry tenant remaining. See
the root `foundry-workshop-plan.md` for the facilitator run-of-show and the session `plan.md` for the reskin
task list.

