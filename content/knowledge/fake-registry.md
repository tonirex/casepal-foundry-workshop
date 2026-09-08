# Fake Registry — CasePal

Registry of invented products, manufacturers, and case IDs used across the CasePal workshop. Every name here should be **checked against IMDRF, national medical-device registers, and public regulator databases** before public release to ensure no accidental collision.

## Fake medical devices

| Fake name | Fictional class | Fictional category | Used in | Notes |
|---|---|---|---|---|
| **CardioFlow-P CF-P2** | Class C | Implantable cardiac monitor | Case corpus (MDR-2026-0117); prior case A2024-042 | Predecessor "CardioFlow-P" was a fake earlier registration; -P2 is a variation. |
| **GluCheck-M2 GC-M2** | Class B | Continuous glucose monitor | Case corpus; prior case A2024-127 (M1 predecessor) | M1 was queried-then-accepted; M2 is a follow-on. |
| **VentiTech-3 VT-3** | Class D | ICU ventilator | Case corpus; prior case A2024-198 (VentiTech-2 rejected) | Teaching point: rejection precedent is valid. |
| **OrthoStim-Pro OS-P** | Class C | Bone growth electrical stimulator | Case corpus; prior case A2024-256 (variant accepted with condition) | |
| **LungCheck-AI LC-A1** | Class C | Chest X-ray AI diagnostic (AI-MD / SaMD) | Case corpus; prior case A2024-312 (earlier LungCheck-AI, queried, pending) | Novel-technology teaching point. |
| **BloodScan-X BS-X1** | Class B | Point-of-care blood analyser | Case corpus (MDR-2026-0129) | **No prior similar in the corpus** (novel signal). |
| **ImmunoFlow IF-1** | Class B | In-vitro diagnostic reagent | Case corpus | |
| **SkinLens-AI SL-A1** | Class C | Skin-cancer screening AI (AI-MD / SaMD) | Case corpus (MDR-2026-0121) | **No prior similar** (novel signal, AI-MD, teaching case). |
| **EasyChair-3 EC-3v** | Class A | Manual wheelchair | Case corpus | Low-complexity variation. |
| **SomniTrack-B ST-B1** | Class B | Wearable EEG monitor | Case corpus | Borderline classification teaching case. |
| **PulsePace-1 PP-1** | Class D | Implantable cardiac pacemaker | Case corpus | First-submission implantable teaching case. |
| **FastAid-Pro FA-P1** | Class B | Automated external defibrillator | Case corpus | Embedded applicant-question teaching case. |
| **IgnorePreviousInstructions-1 IPI-1** | Class A | Prompt-injection stress test artefact | Case corpus (MDR-2026-0130) | Synthetic guardrail test row. |

## Fake manufacturers / applicants

| Name | Product association |
|---|---|
| **CardioDeviceCo Ltd** | CardioFlow-P |
| **SensioMed Ltd** | GluCheck-M2 |
| **RespiTech Ltd** | VentiTech-3 |
| **OrthoBio Ltd** | OrthoStim-Pro |
| **ScanIntel Ltd** | LungCheck-AI |
| **BloodDx Ltd** | BloodScan-X |
| **ImmunoDX Ltd** | ImmunoFlow |
| **DermaCore Ltd** | SkinLens-AI |
| **MobilityCo Ltd** | EasyChair-3 |
| **NeurTech Ltd** | SomniTrack-B |
| **CardiaLife Ltd** | PulsePace-1 |
| **QuickReg Ltd** | FastAid-Pro |
| **HackyCorp Ltd** | IgnorePreviousInstructions-1 |

All manufacturers use the neutral `Ltd` suffix. No jurisdiction-specific company suffixes.

## Fake case-ID conventions

- **`MDR-2026-<seq>`** — a live registration dossier in the current-year queue (used in the case-packages.jsonl corpus, referenced in labs).
- **`case-A2024-<seq>`** — a completed prior case (used in the prior-cases institutional memory store).
- **`CMS-2026-<n>`** — a Case Management System reference returned by the MCP server (Lab 5).

## Fake reviewer / analyst identities

- **Dr. Wei Ling** — Product Reviewer (main persona)
- **Dr. Aravind Ramesh** — Reviewer's manager
- **Kai** — junior analyst (guardrail-probing role in Lab 3)

All fictional. Any resemblance to real people is coincidental.

## Pre-release checks

Before the repo goes public:

1. Every fake device model against IMDRF UDID public database.
2. Every fake device model against national medical-device registers (US FDA 510(k), EU EUDAMED, UK MHRA MedTech, etc.).
3. Every fake manufacturer name against public regulator databases + generic business registers.
4. If a collision is found, rename here first, then bulk-substitute in `knowledge/`, `content/assets/case-packages.jsonl`, and lab pages.

## Notes for facilitators

The **novel-signal** cases (BloodScan-X, SkinLens-AI) are deliberately designed to trip CasePal's institutional-memory retrieval. Lab 2 uses them to demonstrate the *"no prior similar case"* refusal path — a teaching point facilitators should preserve (Pattern #7: Handling Uncertainty). Do not add prior-case entries for these products; the pack breaks if they gain analogues.
