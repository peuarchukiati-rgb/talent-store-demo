# Lab report · LAB-20261121-211140ICT-s1-offline

- suite: **s1**
- mode: **offline**
- timestamp_ict: 2026-11-21 21:11:40 ICT
- git_commit: `4b591f9aba9216a31a27a564ea546c1366f41cc3`
- dirty_tree: False
- models: stub/stub-v1

**Result: 5 PASS · 0 FAIL · 1 NOT RUN**

## Assertions

| id | description | expected | actual | status |
|----|-------------|----------|--------|--------|
| stub.runs | [stub->stub] both runs exit 0 | A ok and B ok | A=True B=True | **PASS** |
| stub.raw_pin | [stub->stub] raw aggregate matches the pinned value throughout | 3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc | before=3bb695fe3b39 afterA=3bb695fe3b39 afterB=3bb695fe3b39 | **PASS** |
| stub.b_skips_done | [stub->stub] B processed only the handoff 'next' list | ['C-006', 'C-007', 'C-008', 'C-009'] | ['C-006', 'C-007', 'C-008', 'C-009'] | **PASS** |
| stub.a_untouched | [stub->stub] A's outputs are byte-identical after B ran | all A files unchanged | unchanged | **PASS** |
| stub.coverage | [stub->stub] all 9 candidates covered exactly once (A + B) | 9 unique, no overlap | 9 ids, 9 unique | **PASS** |
| overlap.divergence | overlap: same candidate through two DIFFERENT models, status diff | status diff reported | only the stub provider exists offline | **NOT RUN** |

## Inputs


## Outputs

- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/A-stub/C-001.md` — `8cd0d411cb7e1159d7cfb9d5c8dcbf065276e8c1736c8c97deda659df8e68c82`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/A-stub/C-002.md` — `03b4ef5f6c8c239e7fff381406862eb0e35c19eec66261504da3d073585c2e2f`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/A-stub/C-003.md` — `6d51c497f36ee853fb3142627990d33df52bfe5993c7cd7ee34a8767aad628ee`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/A-stub/C-004.md` — `13f1d2697240cf25e802c06bb3e2027a38ec9a6c345a1ce79a587fd11f853ba2`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/A-stub/C-005.md` — `26db082932a504e6fae8da3f968ed065b0fd5d19a6c176672f92c0143052dfda`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/B-stub/C-006.md` — `d8a822d7f0af6f2620e4613376e1a2b986c9d7b5c2e61bdc897b6ee6690c92ac`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/B-stub/C-007.md` — `09a18e66d63a71f603ecff10508b982d351b0d9887310b12004e83077d8b77dd`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/B-stub/C-008.md` — `aeab52f7ef3b2b7187dd17d0d0bc76a8bca54a96e053a4c663e1267752a0d52d`
- `lab/work/LAB-20261121-211140ICT-s1-offline-stub/store/curated/B-stub/C-009.md` — `935c906bf2df66cc1eb4fea3a0dc14185445a9991e6a4c177d4a862288ac5b7e`

## Notes

- Offline uses the deterministic stub for both A and B, so A and B are the SAME engine. The continuation MECHANICS (raw unchanged, skip done, A untouched, exact coverage) are proven here; the model-difference and overlap-divergence dimensions require real mode (openai<->claude).
- Swap granularity: the handoff boundary is a whole candidate; A did ['C-001', 'C-002', 'C-003', 'C-004', 'C-005'], B did ['C-006', 'C-007', 'C-008', 'C-009']. No candidate is split across models.

Logs: `lab-reports/LAB-20261121-211140ICT-s1-offline/logs`
