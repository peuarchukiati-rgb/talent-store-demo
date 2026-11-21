---
type: evidence_summary
candidate: C-CTL
candidate_ref: store/raw/candidates/C-CTL.md
candidate_sha256: a29f15fd4fb45dff9cc71f75605a94c85dd4b328312df5be8a1ed2af13487948
jd: JD-SC-014
jd_ref: store/raw/jd/JD-SC-014.md
jd_sha256: 0e47869bc2378ce106dc7975ce4c87ad395d89c4705a7865085ddf859390f8f0
pool: external
run_id: claude-ctl-2
provider: claude_cli
model: sonnet
created_utc: '2026-11-21T14:27:37+00:00'
status: proposed
decided_by: null
scored: false
ranked: false
checks:
  quotes_total: 10
  quotes_verified: 10
  warnings: []
  injection_flags: []
summary: The profile shows about ten years across supply planning at a food company
  and demand planning at a beverage company, with SAP ECC (PP) and SAP IBP use. It
  describes ownership of a monthly demand review, coaching of two junior planners,
  and a forecast error reduction from 31% to 24%. Supply review, sign-off steps and
  shelf-life topics are not described.
evidence:
- id: R1
  status: evidenced
  evidence:
  - quote: '## Demand Planner (2020 – now) · a beverage company, Binh Duong'
    verified: true
  - quote: '## Supply Planner (2016 – 2020) · a food company, Dong Nai'
    verified: true
  note: Roles in beverage and food span 2016 to now, roughly 10 years of demand and
    supply planning.
- id: R2
  status: partial
  evidence:
  - quote: Owns the monthly demand review for 80 beverage SKUs with the sales team.
    verified: true
  note: Monthly demand review is shown, but supply review and sign-off steps are not
    described.
- id: R3
  status: evidenced
  evidence:
  - quote: Builds statistical forecasts in SAP IBP and tracks forecast accuracy (MAPE).
    verified: true
  - quote: Ran weekly supply plans in SAP ECC (PP) and maintained safety-stock data.
    verified: true
  note: Hands-on use of SAP IBP and SAP ECC PP for forecasting and planning data.
- id: R4
  status: evidenced
  evidence:
  - quote: 'Vietnamese (native). English: business level; writes weekly reports for
      the regional team.'
    verified: true
  note: Vietnamese native and business-level English stated, with regional team reporting.
- id: R5
  status: partial
  evidence:
  - quote: Coaches two junior planners on forecast adjustments for promotions.
    verified: true
  note: Coaching of two junior planners is stated, though the scope is limited to
    forecast adjustments.
- id: N1
  status: evidenced
  evidence:
  - quote: Cut forecast error from 31% to 24% between 2022 and 2024.
    verified: true
  note: Forecast error improvement is given with before and after figures.
- id: N2
  status: partial
  evidence:
  - quote: Owns the monthly demand review for 80 beverage SKUs with the sales team.
    verified: true
  note: Beverage experience is shown, but shelf-life considerations are not mentioned.
- id: N3
  status: evidenced
  evidence:
  - quote: Office located inside the Binh Duong factory compound since 2020.
    verified: true
  note: Office is inside a factory compound, though hands-on work on the factory floor
    is not described.
open_points:
- Whether the candidate has run the supply review and monthly sign-off pack, not only
  the demand review.
- Whether the candidate has experience managing shelf-life or expiry-sensitive planning
  parameters such as shelf life master data.
- Whether the coaching of two planners was a formal reporting line or informal guidance.
- Extent of day-to-day interaction with the factory floor in Vietnamese.
---

# Evidence summary · Control Candidate (synthetic) · Demand & Supply Planning Lead

> Pre-screen output. Evidence only: no score, no rank, no recommendation. A person decides.

## Summary

The profile shows about ten years across supply planning at a food company and demand planning at a beverage company, with SAP ECC (PP) and SAP IBP use. It describes ownership of a monthly demand review, coaching of two junior planners, and a forecast error reduction from 31% to 24%. Supply review, sign-off steps and shelf-life topics are not described.

## Evidence by requirement

### R1 · must · `evidenced`
_5+ years in demand planning, supply planning or S&OP in FMCG or food manufacturing_

> "Demand Planner (2020 – now) · a beverage company, Binh Duong" — ✓ verbatim
> "Supply Planner (2016 – 2020) · a food company, Dong Nai" — ✓ verbatim

Roles in beverage and food span 2016 to now, roughly 10 years of demand and supply planning.

### R2 · must · `partial`
_Has run a monthly S&OP / IBP cycle end to end (demand review, supply review, sign-off)_

> "Owns the monthly demand review for 80 beverage SKUs with the sales team." — ✓ verbatim

Monthly demand review is shown, but supply review and sign-off steps are not described.

### R3 · must · `evidenced`
_Hands-on with SAP (APO, IBP or ECC MM/PP) for planning data_

> "Builds statistical forecasts in SAP IBP and tracks forecast accuracy (MAPE)." — ✓ verbatim
> "Ran weekly supply plans in SAP ECC (PP) and maintained safety-stock data." — ✓ verbatim

Hands-on use of SAP IBP and SAP ECC PP for forecasting and planning data.

### R4 · must · `evidenced`
_Business-level English and Vietnamese (works with regional team and factory floor)_

> "Vietnamese (native). English: business level; writes weekly reports for the regional team." — ✓ verbatim

Vietnamese native and business-level English stated, with regional team reporting.

### R5 · must · `partial`
_Has led or coached a team of at least 2 planners_

> "Coaches two junior planners on forecast adjustments for promotions." — ✓ verbatim

Coaching of two junior planners is stated, though the scope is limited to forecast adjustments.

### N1 · nice · `evidenced`
_Forecast accuracy or inventory improvement with a stated before/after figure_

> "Cut forecast error from 31% to 24% between 2022 and 2024." — ✓ verbatim

Forecast error improvement is given with before and after figures.

### N2 · nice · `partial`
_Experience with shelf-life sensitive products (dairy, beverages, culinary)_

> "Owns the monthly demand review for 80 beverage SKUs with the sales team." — ✓ verbatim

Beverage experience is shown, but shelf-life considerations are not mentioned.

### N3 · nice · `evidenced`
_Has worked inside a factory site, not only at head office_

> "Office located inside the Binh Duong factory compound since 2020." — ✓ verbatim

Office is inside a factory compound, though hands-on work on the factory floor is not described.

## Open points to verify

- Whether the candidate has run the supply review and monthly sign-off pack, not only the demand review.
- Whether the candidate has experience managing shelf-life or expiry-sensitive planning parameters such as shelf life master data.
- Whether the coaching of two planners was a formal reporting line or informal guidance.
- Extent of day-to-day interaction with the factory floor in Vietnamese.
