# Contract Review Pack: SaaS Master Subscription Agreement

A complete contract review produced with AutoClaw, for the AutoClaw Round 3 campaign (Legal Practice track).

**The matter is fictional.** Northwind Precision Manufacturing (Ohio) buying a 36-month, US$180,000/year device-telemetry subscription from Skyline Device Cloud. No real customer, contract, or personal data appears anywhere in this repository.

## The finding

Five of the six state privacy statutes in the customer's footprint exclude employment data from "consumer." California does not. Because the platform's data is badge numbers, operator names, and shift records, **California is the only state where that data is protected at all** - and it alone drives the structure of the data processing addendum.

Second finding: the vendor's liability cap is aggressive but likely enforceable for commercial loss. The negotiation targets carve-outs and the cap base, not nullity.

## What is in here

| Path | Contents |
| --- | --- |
| `deliverables/01-vendor-draft.docx` | the vendor's unmodified form, 15 clauses |
| `deliverables/02-redline-tracked-changes.docx` | Word tracked changes: 27 insertions, 25 deletions |
| `deliverables/03-clean-revised.docx` | countersignature-ready text |
| `deliverables/04-review-memo.docx` | clause-by-clause analysis with 15 source links |
| `deliverables/05-risk-matrix.xlsx` | 24 issues: 6 critical, 13 high, 5 medium |
| `deliverables/06-citation-verification-log.docx` | 13 authorities, plus the claims deliberately not made |
| `deliverables/07-reusable-checklist.docx` | 12-point SaaS review checklist |
| `deliverables/08-state-overlay.xlsx` | CA, VA, MD, DE, TX, DC: applicability, DPA terms, clause map |
| `entry/09-review-board.html` | one-page visual summary |
| `HOUSE-STYLE.md` | citation and terminology conventions |

## How it was built

1. Read the vendor form twice: once for structure, once clause by clause, sorting each issue into void, unenforceable as applied, or commercial trade.
2. Tested each clause against the statute that governs it, not against a general sense of unfairness.
3. Verified every authority in the primary source before citing it. Where a rule is commonly mis-cited, the log says so.
4. Redlined as paired edits, so no clause carries both the old rule and its replacement.

Two verifications worth opening the log for: the CCPA service-provider terms are Cal. Civ. Code 1798.100(**d**), not (e); and 16 CFR Part 425 does not currently contain the click-to-cancel duty routinely attributed to it.

## Limits

Statutes and regulations only - no case law, because no case database was reachable during the review. The matter is fictional. This is a work sample, not legal advice.

## Rebuilding

Python 3.13 with `python-docx` and `openpyxl`.

```
python scripts/build_contract_us.py     # vendor draft, redline, clean draft
python scripts/build_risk_matrix_us.py  # risk matrix
python scripts/build_state_overlay.py   # state overlay
python scripts/md_to_docx_us.py         # memo, log, checklist
```
