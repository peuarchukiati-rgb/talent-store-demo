# Lab report · LAB-20261121-211141ICT-s5-offline

- suite: **s5**
- mode: **offline**
- timestamp_ict: 2026-11-21 21:11:41 ICT
- git_commit: `4b591f9aba9216a31a27a564ea546c1366f41cc3`
- dirty_tree: True
- models: stub/stub-v1 python 3.15.0 / pyyaml 6.0.4

**Result: 3 PASS · 0 FAIL · 0 NOT RUN**

## Assertions

| id | description | expected | actual | status |
|----|-------------|----------|--------|--------|
| s5.runs | both repro runs exit 0 | rc 0 and 0 | 0,0 | **PASS** |
| s5.same_fileset | both runs produce the same 9 output files | 9 files, same names | 9 vs 9 | **PASS** |
| s5.byte_identical | every output file is byte-identical across two independent runs | all sha256 equal | all equal | **PASS** |

## Inputs


## Outputs

- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-001.md` — `ba8ba00009daed21a00cf41b4ad5b6035589f3dcabfe6a986e1994f6e384d947`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-002.md` — `2197b2a7f350f39b6b970e38f0732cf3d4ae4461d6487d3eb30dc88202c69822`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-003.md` — `801ff5c4a82c968aa9d930f548a05385186455e142e5bebb91e9417396901eb2`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-004.md` — `a4430a578bb2de95389f2c5a6cf3e050d08bd4c11040c5364f82d4ad99ad5bfb`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-005.md` — `11f2a884de9eac102acc5267b9026bd019f12a64201f4c56250a1c502dc7472c`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-006.md` — `495ea4f2ba51f4dccd0b28ad6499fe57c7af99236f098f29f51a04125c151d83`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-007.md` — `80b9d9b086d47ba70651c26679c1c6097a2c9a238507c5288d227d10dacea6a2`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-008.md` — `62ef9bbeee7fa3cc6fcfd30a37482c6ca35791b84ffbfdab42189d320ceaa5a0`
- `lab/work/LAB-20261121-211141ICT-s5-offline-run1/store/curated/REPRO/C-009.md` — `ddccc1cb24db64c048d345db119f406559dbe86006112c64b2cc68b297713ea0`

## Notes

- Deterministic offline output aggregate sha256: 5160f16dba48215aca1c4b3132d301dae07f0b1561ee56be158b3469897d20ea
- Environment: python 3.15.0, pyyaml 6.0.4. pyyaml is pinned in requirements.txt; SOURCE_DATE_EPOCH=1795305600 (2026-11-22T00:00:00Z) fixes created_utc.
- NOZ can re-run on Linux from a fresh clone and expect this same aggregate, given the same Python minor and pyyaml versions.

Logs: `lab-reports/LAB-20261121-211141ICT-s5-offline/logs`
