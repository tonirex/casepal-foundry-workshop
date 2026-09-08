# IMDRF Risk Classification — Overview

*Plain-language explainer written for the CasePal workshop. Based on publicly documented IMDRF (International Medical Device Regulators Forum) risk-classification principles. Not the verbatim IMDRF text.*

The IMDRF risk-classification framework is used by many national regulators (converged, not identical, across jurisdictions) to sort medical devices into four risk classes: **A** (low), **B** (low-moderate), **C** (moderate-high), and **D** (high).

## Determining factors

Class is driven by the *combination* of:

1. **Duration of contact with the body** — transient (<60 min) / short-term (<30 days) / long-term (≥30 days).
2. **Degree of invasiveness** — non-invasive / surface-invasive / body-orifice invasive / surgically invasive / implantable.
3. **Anatomy involved** — skin / mucosal / body cavity / central circulatory / central nervous / spinal.
4. **Active vs. passive** — devices delivering energy for therapy or diagnosis are usually higher class than passive devices.
5. **Diagnostic vs. therapeutic** — diagnostic devices whose result drives significant intervention are higher class.
6. **Intended use severity** — the consequence if the device malfunctions.

A device that scores high on any single factor typically drives the whole classification up. Class is the *highest* applicable, not the average.

## Class-by-class shorthand

- **Class A** — low risk. Non-invasive, transient contact, no energy delivery. Examples given in SOP-02 §2.
- **Class B** — low-moderate risk. Short-term contact, or diagnostic devices whose output supports (but does not drive) clinical decisions.
- **Class C** — moderate-high risk. Long-term contact, surgically invasive, therapeutic energy delivery, or diagnostic AI-MD.
- **Class D** — high risk. Life-supporting, implantable devices contacting central circulatory / nervous / spinal systems, or life-sustaining active devices.

## Special case: Software as a Medical Device (SaMD)

SaMD is classified using a 2 × 4 matrix (state-of-healthcare-decision × decision-consequence) instead of the invasiveness/contact model. See `samd-basics.md` for the mapping. Most AI-MDs land in Class B or C; only SaMD that *drives* treatment of critical conditions typically reaches Class D.

## Reviewer's role

The IMDRF principles are *guidance*, not a lookup table. Every dossier requires the applicant to declare a class **and** the rationale for that declaration. The Agency reviewer confirms the class per SOP-02.

## Where to read more

Public IMDRF working-group publications are the authoritative source. See `references/regulator-guideline-links.md` for the URL. Never quote from the live IMDRF text in your reply — link, don't clone.
