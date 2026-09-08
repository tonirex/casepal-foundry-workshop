# SOP-02 · Medical Device Risk Classification

**Version:** 4.0
**Owner:** Health Products Regulation Group · Medical Devices Branch
**Effective:** 1 April 2024
**Aligned with:** IMDRF risk-classification principles (see `references/imdrf-risk-classification.md`)

> **Synthetic content for the CasePal Foundry workshop.**

## 1. Purpose

Define how the Agency confirms an applicant's declared risk classification (Class A / B / C / D) for a medical device.

## 2. The four classes at a glance

| Class | Risk level | Typical duration of contact | Invasiveness | Examples of the *kind* of device (illustrative, not authoritative) |
|---|---|---|---|---|
| **A** | Low | Transient, non-invasive | None | Wheelchairs, hospital beds, stethoscopes |
| **B** | Low-moderate | Short-term, minimally invasive | Minor | Contact lenses, wound dressings, most in-vitro diagnostic reagents |
| **C** | Moderate-high | Long-term, invasive; measurement-based diagnostic | Significant | Blood-glucose monitors, ventilators (non-critical), diagnostic AI-MD, orthopaedic implants |
| **D** | High | Life-supporting; long-term implantable; contact with central circulatory or nervous system | Critical | Pacemakers, cardiac stents, mechanical ventilators for life support, implantable defibrillators |

## 3. Determination principles

Class is determined by the **highest applicable** factor across:

1. **Invasiveness** (non-invasive / surface / body-orifice / surgically invasive / implantable).
2. **Duration of contact** (transient <60 min / short-term <30 days / long-term ≥30 days).
3. **Intended purpose** (support / monitor / diagnose / treat / life-support).
4. **Anatomy contacted** (skin / mucosal / central circulatory / central nervous / spinal).
5. **Energy delivery** (none / low-energy / therapeutic-energy / life-sustaining).
6. **For software (SaMD)**: state-of-healthcare-decision × decision-consequence matrix — see `references/samd-basics.md`.

## 4. Reviewer confirmation task

For every incoming dossier, CasePal (and the Reviewer) must:

1. Read the applicant's declared class and rationale.
2. Cross-check against §3 principles.
3. If the applicant's declaration is **consistent**, note "class confirmed" in the extraction output.
4. If **inconsistent**, escalate — do not auto-reclassify. The reviewer decides whether to reclassify and inform the applicant, or query for further rationale.

## 5. AI-MD / SaMD note

AI-based medical devices are usually **Class B or C** depending on the state-of-healthcare-decision (drive / inform) and consequence (serious / non-serious / critical). Novel AI-MDs frequently warrant a query on validation methodology (see SOP-03 §4). CasePal must flag AI-MD dossiers as "novel technology" so the reviewer sees the flag on the queue view.

## 6. Interaction with other SOPs

- Completeness by class: **SOP-01**
- Clinical evaluation by class: **SOP-03**
- Prior-similar check: **SOP-04** (helpful — but a prior similar-classed device does NOT bind the current classification)
