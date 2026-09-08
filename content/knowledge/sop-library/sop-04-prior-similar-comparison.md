# SOP-04 · Prior-Similar-Case Comparison

**Version:** 1.5
**Owner:** Health Products Regulation Group · Medical Devices Branch
**Effective:** 1 September 2024

> **Synthetic content for the CasePal Foundry workshop.**

## 1. Purpose

Define when and how to invoke institutional memory — i.e. searching the completed-case store for similar prior submissions — during review of a new medical-device dossier.

## 2. When to search for prior similar cases

**Always** search when:

- The applicant declares a variation or renewal (prior submissions of the same product family exist by definition — retrieve them).
- The applicant references an equivalent device in their clinical evaluation (SOP-03 §3C).
- The device is a **novel technology** or **AI-MD** (see SOP-02 §5).
- The reviewer wants a sanity check on class determination for an unfamiliar device category.

**Optionally** search when a straightforward Class A / B renewal shows no red flags — in practice the reviewer often skips the search in such cases, but CasePal should offer it.

## 3. What constitutes "similar"

The prior-case store is indexed on multiple fields; a hit at *any* level warrants a look:

| Level | Match criterion | Strength of precedent |
|---|---|---|
| **Same product family** | Same manufacturer + same base product name (e.g. "CardioFlow-P" vs. "CardioFlow-P2") | Strongest — usually a variation |
| **Same manufacturer, similar category** | Same applicant + same device category (e.g. two CGMs from the same MAH) | Strong |
| **Similar category, different manufacturer** | Class + category match, different applicant | Moderate |
| **Same technology, different category** | Same core technology (e.g. AI-based image classification) applied to different clinical use | Weak but useful |

## 4. What to report to the reviewer

For every hit, CasePal must surface:

- The prior case ID (`case-A20YY-<seq>`)
- The prior outcome (`accepted` / `accepted-with-condition` / `queried` / `rejected` / `withdrawn`)
- The **one or two key reasons** the prior decision was reached (from the prior case's decision document).
- A **similarity note** — a short sentence explaining why the prior case is being surfaced.

## 5. When NO prior similar exists

This is a legitimate and common outcome. CasePal must:

- Return `count: 0`
- State plainly: *"No prior similar case in the current corpus."*
- **Never** invent a prior case ID.
- Suggest the reviewer treat the submission as a first-of-kind for classification/comparison purposes.

## 6. Prior-case precedent is advisory, not binding

A rejected precedent does not automatically mean the current submission is rejected. A related accepted precedent does not automatically mean the current submission is accepted. Precedents are **inputs to the reviewer's judgement**, not substitutes for it.
