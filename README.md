# talent-store-demo

A working prototype for one plug on an organisation-owned **store**:
a recruitment pre-screen (BUC-1B, Talent Agent) that writes evidence
summaries into a Markdown store, then re-runs on a second model while
the store stays unchanged.

**All data in this repo is synthetic.** The job description and the nine
candidates (C-001…C-009; three internal, six external, one written in
Vietnamese) are invented for the demo. No real person, client or employer data.

## What it proves

1. **The floor works.** A pre-screen reads one JD and each candidate profile
   from the store and writes an evidence summary per candidate: for each
   requirement, verbatim quotes from the profile, or "not found". Internal
   candidates are shown first as a group. A person (TA / hiring manager)
   records the decision.
2. **Replace runtime, keep state.** The same pre-screen runs on a second
   model. The raw store files are byte-identical before and after both runs
   (sha256 manifest), and each run writes only its own folder.
3. **Reuse the same pool for a new opening.** A second job description is
   screened against the same nine candidates with no re-ingest: every
   candidate file is byte-identical before and after, and the new outputs
   trace back to the same `candidate_sha256`. See the lab's reuse suite.

## Evidence

- `continuation-evidence/` — the recorded two-runtime continuation run
  (hash tables, logs, claims) behind proof 2.
- `lab-reports/` — the reproducible **test lab**: five suites (continuation,
  reuse, prompt injection, erasure, reproducibility), each with a
  machine-readable report and PASS/FAIL/NOT RUN assertions. `SUMMARY.md`
  indexes every run. Anyone can re-run it (see "Run the lab" below).

## Switched off on purpose

- **No scoring, no ranking, no hire/reject recommendation.** The prompt forbids
  it, the output schema has no score field, a post-check flags verdict
  language, and every summary carries `scored: false` and `ranked: false`.
  The engine this grew from could score; here it advises and a person decides.
- **No sensitive attributes.** Profiles hold only role-relevant fields; the
  prompt forbids inferring age, gender, health, religion, ethnicity or nationality.

## Store layout

```
store/
  raw/            immutable source records (read-only files, hashed in MANIFEST.md)
    jd/JD-SC-014.md
    candidates/C-001.md … C-009.md
  curated/        one folder per model run; a run never edits raw or another run
    A-openai-gpt/C-001.md …
    B-claude-sonnet/C-001.md …
  decisions/      human decisions, append-only, one file per candidate
  MANIFEST.md     sha256 of every raw file, written at seal time
```

Every file is Markdown with YAML frontmatter. Summaries point back to the
exact raw file and its hash (`candidate_ref`, `candidate_sha256`, `jd_ref`,
`jd_sha256`), so any agent or person can trace a claim to its source.

Quotes are checked against the source text after each call. A quote that is
not in the profile is marked `⚠ not found in profile`, never silently trusted.

## Models are config

`config/models.json` holds the model profiles. Keys come from environment
variables only. Providers implemented in `talentstore/providers.py`:

| profile  | provider       | status in this demo |
|----------|----------------|---------------------|
| `azure`  | Azure OpenAI   | adapter implemented; proposed default inside the organisation's tenant; **not run here** (needs a tenant endpoint and key) |
| `openai` | OpenAI GPT (local CLI) | run A |
| `claude` | Anthropic Claude (local CLI) | run B |
| `gemini` | Google Gemini API | adapter implemented; not used in the recorded runs |

Where the model endpoint lives (in-country or not) is a deployment setting,
not a code change.

## Run it

Requires Python 3.9+ and `pyyaml`.

```sh
python3 cli.py seal                          # hash raw layer, make it read-only (once)
python3 cli.py verify                        # raw layer still matches the manifest?
python3 cli.py prescreen --model openai --run-id A-openai-gpt
python3 cli.py prescreen --model claude --run-id B-claude-sonnet
python3 cli.py decide C-001 advance --by "TA: <name>" --run A-openai-gpt --note "phone screen"
python3 cli.py hashes > after.txt            # sha256 of every store file
python3 cli.py render                        # build site/index.html (read-only viewer)
```

`runs/` holds the recorded logs and before/after hash lists.

## Run the lab

A reproducible test lab exercises the engine end to end. Offline mode needs
**no API key, no CLI and no network**, and two offline runs produce identical
output hashes.

```sh
make lab                 # all five suites, offline (or: ./lab/run.sh --mode offline)
make lab-3               # one suite (3 = prompt injection); make lab-1 … lab-5
./lab/run.sh --mode real # real mode: local codex + claude CLIs (no API key)
```

Reports land in `lab-reports/<run_id>/` with `SUMMARY.md` at the top. Each suite
runs on a throwaway copy of the store under `lab/work/` (gitignored); the
committed `store/` is never touched.

## Out of scope for this prototype

Interview insights, HRIS/SuccessFactors integration, candidate community,
job scraping or external chat, a second reader on the same pool.
**Access control (tenant identity, role-based permissions) is out of scope**
here — it is a deployment-side concern, not exercised by this demo or its lab.

(Re-using an old pool for a new opening was previously out of scope; it is now
shown — see proof 3 and the lab's reuse suite report.)
