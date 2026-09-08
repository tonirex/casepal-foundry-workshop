# CasePal Knowledge Pack

Grounding corpus for Lab 2 (Foundry IQ / RAG) and reused by Lab 4 (multi-agent). **All content is synthetic.** No real Agency SOP, no real prior case, no real product, no licensed content.

## Structure

| Path | Type | Used in | Notes |
|---|---|---|---|
| `sop-library/sop-01-completeness-check.md` | SOP | Lab 2, Lab 4 | Required documents per risk class |
| `sop-library/sop-02-risk-classification.md` | SOP | Lab 2 | How Class A/B/C/D is determined (per IMDRF) |
| `sop-library/sop-03-clinical-evaluation.md` | SOP | Lab 2, Lab 4 | Clinical evaluation report requirements |
| `sop-library/sop-04-prior-similar-comparison.md` | SOP | Lab 2, Lab 4 | When and how to invoke institutional memory |
| `sop-library/sop-05-query-drafting.md` | SOP | Lab 4 | Standards for Request-For-Information letters |
| `prior-cases/case-A2024-042-cardioflow-p-predecessor.md` | Prior case decision | Lab 2, Lab 4 | Class C monitor — accepted |
| `prior-cases/case-A2024-127-glucheck-m1.md` | Prior case decision | Lab 2 | Class B CGM — queried, then accepted |
| `prior-cases/case-A2024-198-ventitech-2.md` | Prior case decision | Lab 2 | Class D ventilator — rejected |
| `prior-cases/case-A2024-256-orthostim-variant.md` | Prior case decision | Lab 2, Lab 4 | Class C — accepted with condition |
| `prior-cases/case-A2024-312-lungcheck-ai.md` | Prior case decision | Lab 2 | Class C AI-MD — queried, pending |
| `references/imdrf-risk-classification.md` | Reference (own words) | Lab 2 | Public IMDRF risk-class overview |
| `references/clinical-evaluation-principles.md` | Reference (own words) | Lab 2 | High-level clinical evaluation concepts |
| `references/dossier-structure-overview.md` | Reference (own words) | Lab 2 | Generic dossier anatomy — cover letter → tech file → labelling |
| `references/samd-basics.md` | Reference (own words) | Lab 2 | Software-as-a-Medical-Device essentials |
| `references/regulator-guideline-links.md` | Link-only reference | Lab 2 | Points to public IMDRF/WHO/ICH resources |

## Ground truths encoded in the pack

Lab 2 asks CasePal *"are the requirements met?"* and *"has anything similar been reviewed before?"* The correct answer depends on this corpus. It is designed so:

**SOP references:**
- Class C completeness requirement → cite `sop-01-completeness-check.md` §Class C.
- Risk classification rationale check → cite `sop-02-risk-classification.md`.
- Clinical evaluation adequacy → cite `sop-03-clinical-evaluation.md`.
- When to look for prior similar → cite `sop-04-prior-similar-comparison.md`.
- Query letter drafting → cite `sop-05-query-drafting.md`.

**Prior-case matches (institutional memory):**
- CardioFlow-P (Class C implantable cardiac monitor) → prior similar: `case-A2024-042` (predecessor product, accepted).
- GluCheck-M2 (Class B CGM) → prior similar: `case-A2024-127` (M1 predecessor, queried-then-accepted; workshop teaching point: "queried then accepted" is a common resolution).
- VentiTech-3 (Class D ventilator) → prior similar: `case-A2024-198` (VentiTech-2, **rejected** — teaching point: rejection is a valid signal).
- OrthoStim-Pro (Class C bone-growth stimulator variant) → prior similar: `case-A2024-256` (accepted with condition).
- LungCheck-AI (Class C AI-MD) → prior similar: `case-A2024-312` (older AI-MD, queried and pending — teaching point: novel technology often needs a query).
- **BloodScan-X (Class B blood analyser) → NO prior similar** (novel signal — CasePal must say so).
- **SkinLens-AI (Class C skin-cancer screening AI) → NO prior similar** (novel signal).

## Fake product / manufacturer policy

- All device model numbers, applicant names, and case IDs invented for this workshop.
- Every name is registered in `fake-registry.md` with a pre-release collision-check policy against IMDRF/national medical-device registers.

## Ingestion into Foundry IQ

1. `az storage blob upload-batch` this folder into the workshop's grounding blob container.
2. Create/refresh the Foundry IQ index named `casepal-knowledge` pointing at the container.
3. Share the index with the shared Foundry project (facilitator identity only).
4. Verify a query for `CardioFlow` returns `case-A2024-042` in the top-3.
