# Lab report · LAB-20261121-233110ICT-s4-offline

- suite: **s4**
- mode: **offline**
- timestamp_ict: 2026-11-21 23:31:10 ICT
- git_commit: `4b975087727cf216cc652571692a7b0fcfc8dbfd`
- dirty_tree: False
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

- `store/raw/candidates/C-001.md` — `ccedc5140f0ba47642b5cf57d63390d46a8400553bd81700da3743b5333aa46d`
- `store/raw/candidates/C-002.md` — `028543c0acb1042c61bbd507f25557f0e9d3fb501a3f384eb28122f60f1949a9`
- `store/raw/candidates/C-003.md` — `29038e4906a4de6b2cf7e23d5985b18b031ec03ed48316ada82ed69ad2830ed2`
- `store/raw/candidates/C-004.md` — `7c2602c12c2d55504df5e7f26dbb120e4c6e6eff6cbadf3e2868fd96d5c5cdd5`
- `store/raw/candidates/C-005.md` — `91e2364f2637b6d5ab5d7add88d832dabdefe4b8a86950c4f1bbcbf91d0ae72d`
- `store/raw/candidates/C-006.md` — `8507f8e5c645bf7a3e6eead0074addfdbef92cf1c0409a055a56b0f798f651fe`
- `store/raw/candidates/C-007.md` — `774b53bed292fc3d194be9e0cbfb88ac25f346677106a2aacd7c18f46138b82e`
- `store/raw/candidates/C-008.md` — `a5a3aefd9de197cc953212e9baa50d7e61d0900ea0f3f87c63b79588e2926760`
- `store/raw/candidates/C-009.md` — `c0ae28d746ab8930e6e07c803af15c5316c05bc154b9580bcc62656a97d86256`
- `store/raw/jd/JD-SC-014.md` — `0e47869bc2378ce106dc7975ce4c87ad395d89c4705a7865085ddf859390f8f0`

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

Logs: `lab-reports/LAB-20261121-233110ICT-s4-offline/logs`
