# Medical Device Registration Dossier — Structure Overview

*Plain-language explainer written for the CasePal workshop. Reflects the common structure used by many regulators — the specific section numbers vary between jurisdictions.*

A medical-device registration dossier is a bundle of technical, clinical, and quality documents submitted to a regulator to seek permission to market a device. The bundle can be tens to hundreds of documents; the internal structure is largely converged across regulators.

## Typical top-level anatomy

| Section | Contents | Typical filename patterns |
|---|---|---|
| **1. Cover letter & application form** | Applicant identity, product name, class declaration, submission type (new / variation / renewal), contact details | `01-application-form.pdf`, `02-cover-letter.pdf` |
| **2. Product information** | Description, indication for use, target population, contra-indications, packaging | `03-product-info.pdf`, `04-labels.pdf` |
| **3. Risk classification rationale** | Applicant's classification declaration + justification per IMDRF principles | `05-risk-class.pdf` |
| **4. Design & manufacturing** | Device drawings, materials, manufacturing site, quality-management summary | `06-design.pdf`, `07-manufacturing.pdf`, `08-qms.pdf` |
| **5. Performance testing** | Analytical performance, precision / accuracy / repeatability (measurement devices), biocompatibility (patient-contact), sterilisation validation (sterile devices) | `09-precision.pdf`, `10-biocompat.pdf`, `11-sterilisation.pdf` |
| **6. Clinical evaluation report** | Literature review, equivalence claims, own clinical data, benefit-risk analysis | `12-cer.pdf` |
| **7. Software life-cycle** *(where applicable)* | Software architecture, verification & validation, cybersecurity risk assessment, AI-MD training-data documentation | `13-software.pdf`, `14-cybersecurity.pdf`, `15-ai-validation.pdf` |
| **8. Labelling & IFU** | Primary labelling, secondary labelling, Instructions for Use (final version) | `16-labels.pdf`, `17-ifu.pdf` |
| **9. Post-market plan** | PMS plan; PMCF plan (Class D, some C) | `18-pms-plan.pdf`, `19-pmcf-plan.pdf` |

## Typical size

- **Class A** dossier: 10–30 documents, ~50–100 pages total.
- **Class B**: 15–40 documents, ~100–250 pages.
- **Class C**: 20–50 documents, ~250–500 pages.
- **Class D**: 30–80+ documents, ~500–1000+ pages.

CasePal's intake job scales accordingly — a Class D dossier will require more extraction work and more retrieval hops than a Class A.

## Reading order for the reviewer

Reviewers typically start with the cover letter → application form → product info to build a mental model, then go directly to the class-specific risk-critical sections (CER for Class C+, cybersecurity + PMCF for Class D). CasePal follows the same order: extract the metadata first, then the class-specific gates.

## What CasePal extracts (Lab 1 JSON contract)

At intake, CasePal returns:

```json
{
  "case_id": "...",
  "applicant": "...",
  "device": {
    "name": "...",
    "declared_class": "A|B|C|D",
    "indication_for_use": "..."
  },
  "submission_type": "new|variation|renewal",
  "documents_present": ["01-application-form", "02-cover-letter", ...],
  "documents_missing_for_class": ["12-cer"],
  "priority_flags": ["novel_technology", "ai_md", "safety_incident_on_file"],
  "router_choice": "gpt-5-mini|gpt-5"
}
```

The reviewer sees this as the queue view. The presence of any `documents_missing_for_class` entry automatically routes the dossier to the "query" branch downstream (Lab 4). The presence of a `priority_flags` entry raises the reviewer-attention level.
