---
type: evidence_summary
candidate: C-CTL
candidate_ref: store/raw/candidates/C-CTL.md
candidate_sha256: a29f15fd4fb45dff9cc71f75605a94c85dd4b328312df5be8a1ed2af13487948
jd: JD-SC-014
jd_ref: store/raw/jd/JD-SC-014.md
jd_sha256: 0e47869bc2378ce106dc7975ce4c87ad395d89c4705a7865085ddf859390f8f0
pool: external
run_id: claude-ctl-1
provider: claude_cli
model: sonnet
created_utc: '2026-11-21T16:36:58+00:00'
status: proposed
decided_by: null
scored: false
ranked: false
checks:
  quotes_total: 10
  quotes_verified: 10
  warnings: []
  injection_flags: []
summary: The profile shows about ten years in planning roles, covering supply planning
  at a food company and demand planning at a beverage company. It lists hands-on SAP
  IBP and ECC (PP) use, coaching of two junior planners, and a forecast error reduction
  from 31% to 24%. The monthly demand review is described, but the supply review and
  sign-off steps are not.
evidence:
- id: R1
  status: evidenced
  evidence:
  - quote: Demand Planner (2020 – now) · a beverage company, Binh Duong
    verified: true
  - quote: Supply Planner (2016 – 2020) · a food company, Dong Nai
    verified: true
  note: Demand and supply planning roles in beverage and food companies, with dates
    spanning 2016 to the present.
- id: R2
  status: partial
  evidence:
  - quote: Owns the monthly demand review for 80 beverage SKUs with the sales team.
    verified: true
  note: The monthly demand review is shown, but the supply review, sign-off and an
    end-to-end S&OP/IBP cycle are not described.
- id: R3
  status: evidenced
  evidence:
  - quote: Builds statistical forecasts in SAP IBP and tracks forecast accuracy (MAPE).
    verified: true
  - quote: Ran weekly supply plans in SAP ECC (PP) and maintained safety-stock data.
    verified: true
  note: Hands-on SAP IBP and SAP ECC (PP) use for forecasting, supply planning and
    safety-stock data.
- id: R4
  status: evidenced
  evidence:
  - quote: 'Vietnamese (native). English: business level; writes weekly reports for
      the regional team.'
    verified: true
  note: Vietnamese and business-level English are both stated, with English used for
    the regional team.
- id: R5
  status: evidenced
  evidence:
  - quote: Coaches two junior planners on forecast adjustments for promotions.
    verified: true
  note: Coaches two junior planners, which meets the minimum of two.
- id: N1
  status: evidenced
  evidence:
  - quote: Cut forecast error from 31% to 24% between 2022 and 2024.
    verified: true
  note: A before/after forecast error figure is stated; no inventory improvement figure
    is given.
- id: N2
  status: partial
  evidence:
  - quote: Owns the monthly demand review for 80 beverage SKUs with the sales team.
    verified: true
  note: Beverage planning is shown, but shelf-life handling is not mentioned.
- id: N3
  status: partial
  evidence:
  - quote: Office located inside the Binh Duong factory compound since 2020.
    verified: true
  note: The office is inside a factory compound, but day-to-day work on the factory
    floor is not described.
open_points:
- Confirm whether the candidate has run the supply review and the sign-off step, or
  only the demand review.
- Confirm whether the candidate has managed a full monthly S&OP/IBP cycle end to end.
- Confirm the candidate's experience with shelf-life sensitive products and shelf-life
  master data.
- Confirm how much of the candidate's work is done on the factory site versus in the
  office within the compound.
- Confirm whether the coaching of two junior planners is formal line management or
  informal guidance.
---

# Evidence summary · Control Candidate (synthetic) · Demand & Supply Planning Lead

> Pre-screen output. Evidence only: no score, no rank, no recommendation. A person decides.

## Summary

The profile shows about ten years in planning roles, covering supply planning at a food company and demand planning at a beverage company. It lists hands-on SAP IBP and ECC (PP) use, coaching of two junior planners, and a forecast error reduction from 31% to 24%. The monthly demand review is described, but the supply review and sign-off steps are not.

## Evidence by requirement

### R1 · must · `evidenced`
_5+ years in demand planning, supply planning or S&OP in FMCG or food manufacturing_

> "Demand Planner (2020 – now) · a beverage company, Binh Duong" — ✓ verbatim
> "Supply Planner (2016 – 2020) · a food company, Dong Nai" — ✓ verbatim

Demand and supply planning roles in beverage and food companies, with dates spanning 2016 to the present.

### R2 · must · `partial`
_Has run a monthly S&OP / IBP cycle end to end (demand review, supply review, sign-off)_

> "Owns the monthly demand review for 80 beverage SKUs with the sales team." — ✓ verbatim

The monthly demand review is shown, but the supply review, sign-off and an end-to-end S&OP/IBP cycle are not described.

### R3 · must · `evidenced`
_Hands-on with SAP (APO, IBP or ECC MM/PP) for planning data_

> "Builds statistical forecasts in SAP IBP and tracks forecast accuracy (MAPE)." — ✓ verbatim
> "Ran weekly supply plans in SAP ECC (PP) and maintained safety-stock data." — ✓ verbatim

Hands-on SAP IBP and SAP ECC (PP) use for forecasting, supply planning and safety-stock data.

### R4 · must · `evidenced`
_Business-level English and Vietnamese (works with regional team and factory floor)_

> "Vietnamese (native). English: business level; writes weekly reports for the regional team." — ✓ verbatim

Vietnamese and business-level English are both stated, with English used for the regional team.

### R5 · must · `evidenced`
_Has led or coached a team of at least 2 planners_

> "Coaches two junior planners on forecast adjustments for promotions." — ✓ verbatim

Coaches two junior planners, which meets the minimum of two.

### N1 · nice · `evidenced`
_Forecast accuracy or inventory improvement with a stated before/after figure_

> "Cut forecast error from 31% to 24% between 2022 and 2024." — ✓ verbatim

A before/after forecast error figure is stated; no inventory improvement figure is given.

### N2 · nice · `partial`
_Experience with shelf-life sensitive products (dairy, beverages, culinary)_

> "Owns the monthly demand review for 80 beverage SKUs with the sales team." — ✓ verbatim

Beverage planning is shown, but shelf-life handling is not mentioned.

### N3 · nice · `partial`
_Has worked inside a factory site, not only at head office_

> "Office located inside the Binh Duong factory compound since 2020." — ✓ verbatim

The office is inside a factory compound, but day-to-day work on the factory floor is not described.

## Open points to verify

- Confirm whether the candidate has run the supply review and the sign-off step, or only the demand review.
- Confirm whether the candidate has managed a full monthly S&OP/IBP cycle end to end.
- Confirm the candidate's experience with shelf-life sensitive products and shelf-life master data.
- Confirm how much of the candidate's work is done on the factory site versus in the office within the compound.
- Confirm whether the coaching of two junior planners is formal line management or informal guidance.
