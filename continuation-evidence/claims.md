# Claims - what is SHOWN vs PROPOSED

Each claim is tagged SHOWN (it actually ran, here, with evidence on disk) or PROPOSED
(designed/argued, not demonstrated in this run). Evidence paths are relative to repo root
`~/talent-store-demo`.

## SHOWN (ran in this demo, 2026-11-21 UTC)

| # | Claim | Evidence | Status |
|---|---|---|---|
| 1 | A sequential handoff-continuation runs across two different runtimes. | continuation-evidence/run-A.log, continuation-evidence/run-B.log | SHOWN |
| 2 | Run A = OpenAI GPT-5.6 via local Codex CLI (no API key) pre-screened C-001–C-005. | run-A.log; store/curated/A-openai/C-00[1-5].md | SHOWN |
| 3 | Run A wrote a readable handoff H-001 with done+next lists, per-candidate output paths + sha256, and a pinned raw-manifest sha. | store/handoffs/H-001.md; continuation-evidence/shot1-H-001.png | SHOWN |
| 4 | Run B = Claude Sonnet via local Claude CLI resumed from H-001, processed ONLY the `next` list (C-006–C-009), and explicitly logged skipping A's done list. | run-B.log; continuation-evidence/shot2-B-resume-log.png | SHOWN |
| 5 | All 9 candidates ended pre-screened across TWO runtimes via one handoff. | store/curated/A-openai/ (5) + store/curated/B-claude/ (4) | SHOWN |
| 6 | The raw store is byte-identical before A, after A, and after B ("keep state"). | continuation-evidence/hash-table.md; `cli.py verify` printed "raw layer OK: matches manifest" at all three points | SHOWN |
| 7 | Run B did not touch run A's curated folder (A's 5 sha256 identical before/after B). | continuation-evidence/hash-table.md (A-untouched table) | SHOWN |
| 8 | Every quote in the outputs is checked verbatim against the source profile; unverifiable quotes are flagged, not trusted. | talentstore/prescreen.py `_check`; `checks.quotes_verified` in each curated .md | SHOWN |
| 9 | The feature is additive and surgical: new `--candidates`, `--handoff`, `--resume` options; default `prescreen` behaviour unchanged. | git diff on cli.py + talentstore/prescreen.py | SHOWN |

## PROPOSED (designed, NOT demonstrated here)

| # | Claim | Status |
|---|---|---|
| A | The same handoff mechanism carries state to any other runtime (Azure OpenAI, Gemini) the config lists. | PROPOSED - only openai + claude ran |
| B | This replaces a single-vendor pre-screen pipeline inside an organisation's own tenant. | PROPOSED |

## NOT proven (explicit - do not over-read the demo)

- Candidate and JD data are SYNTHETIC. No real applicant data was used.
- NOT tested on Nestlé systems, tenant, SSO, or data. Local macOS only.
- The Azure OpenAI path (config profile `azure`, the proposed in-tenant default) was NOT run - no endpoint/key present; it would raise "endpoint/key not set". Only the two CLI-bridge providers ran.
- The Gemini path was NOT run.
- No scoring, ranking, or hire/reject recommendation is produced or claimed - by design the tool emits evidence only; a human decides.
- Runtimes ran via local CLI bridges (Codex CLI, Claude CLI) on one machine; no cloud/enterprise deployment, latency, or scale was tested.
- Model output quality was not independently graded beyond the built-in verbatim-quote and banned-verdict-language checks.
