# AutoClaw Round 3 - Legal Practice entry

A contract review work sample built end to end with AutoClaw, for the AutoClaw Round 3 campaign
(Legal Practice track, November 5-20, 2026).

**Start here: [work/round3/README.md](work/round3/README.md)**

## What it is

A vendor-drafted SaaS master subscription agreement, reviewed the way a lawyer would deliver it:
a Word redline, a clean revised draft, a clause-by-clause memo, a risk matrix, a six-jurisdiction
privacy overlay, a citation verification log, and a reusable checklist.

The matter is fictional: Northwind Precision Manufacturing (Ohio) buying a 36-month,
US$180,000/year device-telemetry subscription from Skyline Device Cloud. No real customer,
contract, or personal data appears anywhere in this repository.

## The headline finding

Five of the six state privacy statutes in the customer's footprint exclude employment data from
"consumer." California does not. Because the platform's data is badge numbers, operator names,
and shift records, California is the only state where that data is protected at all - and it
alone shapes the data processing addendum.

## Repository layout

```
work/round3/           the entry: deliverables, entry pack, matter brief
work/round3/README.md  the entry landing page
scripts/               the builders that generate every document
docs/prompts-history/  dated record of each working session
```

Every document is generated from source data, so the review can be re-run rather than retyped:

```
python scripts/build_contract_us.py
python scripts/build_risk_matrix_us.py
python scripts/build_state_overlay.py
python scripts/md_to_docx_us.py
```

## Limits

Statutes and regulations only - no case law, because no case database was reachable during the
review. The matter is fictional. This is a work sample, not legal advice.
