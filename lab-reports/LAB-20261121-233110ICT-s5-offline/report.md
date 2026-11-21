# Lab report · LAB-20261121-233110ICT-s5-offline

- suite: **s5**
- mode: **offline**
- timestamp_ict: 2026-11-21 23:31:10 ICT
- git_commit: `4b975087727cf216cc652571692a7b0fcfc8dbfd`
- dirty_tree: False
- models: stub/stub-v1 python 3.15.0 / pyyaml 6.0.4

**Result: 3 PASS · 0 FAIL · 0 NOT RUN**

## Assertions

| id | description | expected | actual | status |
|----|-------------|----------|--------|--------|
| s5.runs | both repro runs exit 0 | rc 0 and 0 | 0,0 | **PASS** |
| s5.same_fileset | both runs produce the same 9 output files | 9 files, same names | 9 vs 9 | **PASS** |
| s5.byte_identical | every output file is byte-identical across two independent runs | all sha256 equal | all equal | **PASS** |

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

- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-001.md` — `ba8ba00009daed21a00cf41b4ad5b6035589f3dcabfe6a986e1994f6e384d947`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-002.md` — `2197b2a7f350f39b6b970e38f0732cf3d4ae4461d6487d3eb30dc88202c69822`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-003.md` — `801ff5c4a82c968aa9d930f548a05385186455e142e5bebb91e9417396901eb2`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-004.md` — `a4430a578bb2de95389f2c5a6cf3e050d08bd4c11040c5364f82d4ad99ad5bfb`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-005.md` — `11f2a884de9eac102acc5267b9026bd019f12a64201f4c56250a1c502dc7472c`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-006.md` — `495ea4f2ba51f4dccd0b28ad6499fe57c7af99236f098f29f51a04125c151d83`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-007.md` — `80b9d9b086d47ba70651c26679c1c6097a2c9a238507c5288d227d10dacea6a2`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-008.md` — `62ef9bbeee7fa3cc6fcfd30a37482c6ca35791b84ffbfdab42189d320ceaa5a0`
- `lab/work/LAB-20261121-233110ICT-s5-offline-run1/store/curated/REPRO/C-009.md` — `ddccc1cb24db64c048d345db119f406559dbe86006112c64b2cc68b297713ea0`

## Notes

- Deterministic offline output aggregate sha256: 5160f16dba48215aca1c4b3132d301dae07f0b1561ee56be158b3469897d20ea
- Environment: python 3.15.0, pyyaml 6.0.4. pyyaml is pinned in requirements.txt; SOURCE_DATE_EPOCH=1795305600 (2026-11-22T00:00:00Z) fixes created_utc.
- A reviewer can re-run on Linux from a fresh clone and expect this same aggregate, given the same Python minor and pyyaml versions.

Logs: `lab-reports/LAB-20261121-233110ICT-s5-offline/logs`
