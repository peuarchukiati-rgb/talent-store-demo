# Lab report · LAB-20261121-211141ICT-s4-offline

- suite: **s4**
- mode: **offline**
- timestamp_ict: 2026-11-21 21:11:41 ICT
- git_commit: `4b591f9aba9216a31a27a564ea546c1366f41cc3`
- dirty_tree: True
- models: stub/stub-v1

**Result: 6 PASS · 0 FAIL · 0 NOT RUN**

## Assertions

| id | description | expected | actual | status |
|----|-------------|----------|--------|--------|
| s4.present_before | C-004 is present across the store + site before erasure | hits in raw/curated/decisions/handoffs/site | 23 file-hits | **PASS** |
| s4.zero_hits | after erasure, C-004 id/name/unique-strings return zero hits everywhere | 0 hits across raw, curated, decisions, handoffs, MANIFEST, site | 0 hits ({}) | **PASS** |
| s4.verify_after | raw layer still verifies after erasure + re-seal | raw layer OK | raw layer OK: matches manifest | **PASS** |
| s4.unrelated_intact | files unrelated to the erased candidate keep their sha256 | no unrelated file changed | all intact | **PASS** |
| s4.changeset_bounded | only the target's files are removed; only MANIFEST + handoff are re-written | removed = C-004 traces; changed = MANIFEST.md + handoffs | removed 6 file(s); changed ['H-001.md', 'MANIFEST.md'] | **PASS** |
| s4.guard_default_store | erase refuses to run against the committed store/ | non-zero exit, 'refusing to erase' | refused | **PASS** |

## Inputs


## Outputs


## Notes

- removed: curated/A-openai/C-004.md (was sha256:0c40aac0053b51fe...)
- removed: curated/A-openai-gpt/C-004.md (was sha256:a109ea38d8a79da7...)
- removed: curated/B-claude-sonnet/C-004.md (was sha256:d1f20a2234c00ff4...)
- removed: curated/LABRUN/C-004.md (was sha256:848b21637e4e6fb4...)
- removed: decisions/C-004.md (was sha256:565dc1530e0ffa4b...)
- removed: raw/candidates/C-004.md (was sha256:7c2602c12c2d5550...)
- re-written: MANIFEST.md sha256 cacbc5e8120f... -> b8a52fbe56b5...
- re-written: handoffs/H-001.md sha256 7a5f9a2a2510... -> 9b087e7ee2ed...
- HONEST LIMIT — Git history: this erasure cleans the working store, but the candidate's content still exists in Git history (commit 42ff14c). The data here is synthetic, so there is no harm. Production deletion of real PII would require: no Git as the system of record for PII; deletion across the store, search indexes, backups, logs and the model provider's retention; and a deletion RECORD that itself holds no PII.
- Run on a lab store copy only; the committed store/ was never touched (guard enforced).

Logs: `lab-reports/LAB-20261121-211141ICT-s4-offline/logs`
