# Prior Case A2024-312 — LungCheck-AI (earlier version)

**Case ID:** case-A2024-312
**Applicant:** ScanIntel Ltd *(fictional)*
**Product:** LungCheck-AI (base model) — Class C AI-MD / SaMD chest X-ray diagnostic aid
**Submission type:** New registration
**Query issued:** 25 September 2024
**Response received:** 20 November 2024 (partial)
**Second query issued:** 5 December 2024
**Status:** ⏸️ **Pending** (as of end 2024)

> **Synthetic content for the CasePal Foundry workshop.**

## Summary

A chest-X-ray AI diagnostic aid intended to flag suspected pulmonary opacities for radiologist review. Class C — SaMD, informs a clinical decision with non-critical consequence (radiologist retains diagnostic authority).

## Query trajectory

Because AI-MDs are a novel-technology category (SOP-02 §5), the reviewer flagged this dossier for close scrutiny at intake. The clinical evaluation report (SOP-03 §4) is where most queries have concentrated:

**First RFI (September 2024):**

1. Training-data provenance — provide the demographic breakdown of the training set.
2. Validation methodology — hold-out test set characteristics, per-subgroup performance.
3. Real-world monitoring plan for model drift.
4. Model version binding — which version of the model is being registered.

**Applicant response (November 2024):**

Provided training-data documentation. Validation methodology was partial — no per-subgroup performance data. Model-version binding clear.

**Second RFI (December 2024):**

Requested subgroup performance metrics with confidence intervals per SOP-03 §4.

## Why still pending

At the time of writing, the applicant response to the second RFI is due. Case remains open in the store.

## Why this precedent is useful

Teaching points:

- **Novel technology often takes multiple RFI cycles.** This is *expected*, not evidence of a bad dossier.
- **AI-MD validation subgroup performance is a recurring gap.** CasePal should proactively surface this SOP-03 §4 requirement whenever an AI-MD is being extracted.
- **"Pending" is a first-class outcome in the store** — the workshop teaches that CasePal should never invent an outcome for still-open cases. When Wei Ling asks *"has LungCheck-AI been reviewed before?"* the correct answer is *"there is an open prior case — outcome pending"*.
