# Software as a Medical Device (SaMD) — Basics

*Plain-language explainer written for the CasePal workshop. Based on publicly documented IMDRF SaMD principles.*

**SaMD** — Software as a Medical Device — is software intended for one or more medical purposes, performing those purposes *without being part of* a hardware medical device. Examples include diagnostic imaging AI, decision-support software, monitoring apps that connect to consumer sensors, and treatment-planning tools.

## The SaMD 2 × 4 risk matrix

Unlike hardware devices (classified by invasiveness / duration / anatomy), SaMD is classified by the intersection of:

**Axis 1 — State of healthcare situation or condition:**
- **Non-serious** — routine care, wellness.
- **Serious** — moderately severe medical condition.
- **Critical** — life-threatening or high-morbidity condition.

**Axis 2 — Significance of information provided to healthcare decision:**
- **Inform clinical management** — the software's output supports a clinician's decision (which retains authority).
- **Drive clinical management** — the software's output is used to determine a next diagnostic or therapeutic action (informs but does not treat).
- **Treat or diagnose** — the software's output is used directly to treat or diagnose (highest impact).

The intersection determines SaMD risk category (I / II / III / IV in IMDRF nomenclature), which most national regulators then map to their Class A/B/C/D framework.

## Rough Class mapping used by the Agency (this workshop)

| SaMD IMDRF category | Agency class |
|---|---|
| I (inform + non-serious) | Class B |
| II (drive + non-serious, or inform + serious) | Class B |
| III (drive + serious, or inform + critical, or treat/diagnose + non-serious) | Class C |
| IV (drive + critical, or treat/diagnose + serious/critical) | Class D |

Most AI-MDs currently under review are IMDRF II–III → Agency Class B–C.

## AI-MD is a subset of SaMD

An **AI-MD** is a SaMD whose core function uses machine learning (or another AI technique). The IMDRF SaMD framework applies. Additionally, AI-MDs raise specific evaluation concerns that ordinary SaMD does not:

- **Training-data provenance and representativeness** — is the training population representative of the deployment population?
- **Validation-set characteristics** — hold-out test methodology, per-subgroup performance metrics.
- **Model drift** — does model performance change as clinical practice evolves?
- **Model-version binding** — which model version is registered, and how are updates managed?

See SOP-03 §4 for the specific query template for AI-MD dossiers with gaps in these areas.

## Reviewer takeaways

- SaMD is classified by intended use, not by the hardware it runs on.
- AI-MD adds validation-and-monitoring concerns on top of ordinary SaMD.
- The clinical evaluation for AI-MD is currently the most common source of RFI queries. See prior case A2024-312 for a live example.
