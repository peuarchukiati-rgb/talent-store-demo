# Lab report · LAB-20261121-233110ICT-s2-offline

- suite: **s2**
- mode: **offline**
- timestamp_ict: 2026-11-21 23:31:10 ICT
- git_commit: `4b975087727cf216cc652571692a7b0fcfc8dbfd`
- dirty_tree: False
- models: stub/stub-v1

**Result: 5 PASS · 0 FAIL · 0 NOT RUN**

## Assertions

| id | description | expected | actual | status |
|----|-------------|----------|--------|--------|
| s2.runs | both screening runs exit 0 | rc 0 and rc 0 | jd1=0 jd2=0 | **PASS** |
| s2.candidates_identical | every candidate file sha256 identical before vs after (no re-ingest) | all 9 identical | all identical | **PASS** |
| s2.jd1_untouched | JD-1 outputs are byte-identical after the JD-2 run | unchanged | unchanged | **PASS** |
| s2.ref_back | JD-2 outputs carry the raw candidate_sha256 (traceable to source) | all match raw file hash | all match | **PASS** |
| s2.new_question | same pool yields a DIFFERENT status map for the new JD | >=1 candidate differs JD-1 vs JD-2 | 9 candidate(s) differ | **PASS** |

## Inputs

- `lab/fixtures/JD-DP-021.md` — `91e1dd605c5f921fc3572670d71dec905abf2b71791357ddad1495cd7b9c07ce`

## Outputs

- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-001.md` — `fbccc7372628121e69cde95a550beb48e4b009e8d37ea84aef149f5bc48edec7`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-002.md` — `9c145abd5cb81ee76246004a0a4b6b200951854a6ab6ab983300834dec1824f8`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-003.md` — `4facf77f7e492d6e29a9e0995bc9729a3e49b0b35b9d90a1ce357cb92a2e59c9`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-004.md` — `687e0f186c52b9d9fb3726026b010a0fccb72c4e62cbe32713c130e4f0a2d792`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-005.md` — `cbf7565757b365ca6eb12359d2de4237763de807989fd2659dc59294f07cec42`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-006.md` — `759929afc15ea3e4dc4fe04358812f1ecd485275352c05040a624991e1de5f3c`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-007.md` — `3df28a12c68591c9135bbecc8d63591b1f72c75d257009bf5db2b38d7387e4bc`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-008.md` — `1011743ca12c7fdbe678c6d813b9450b65da902e7762c04ad20997ba496d43e8`
- `lab/work/LAB-20261121-233110ICT-s2-offline/store/curated/JD2/C-009.md` — `1b7ddda1211a67a0b0cba61f1031b89f7e472dcdc4d87f8f65aa83e2b0a18d11`

## Notes

- Per-candidate status diff JD-1(JD-SC-014) vs JD-2(JD-DP-021): {'C-001': {'N2': ('evidenced', None), 'N3': ('evidenced', None), 'R6': (None, 'evidenced'), 'N1': ('partial', None)}, 'C-002': {'N2': ('not_found', None), 'N3': ('partial', None), 'R6': (None, 'partial'), 'N1': ('partial', None), 'R5': ('not_found', 'partial'), 'R2': ('evidenced', 'partial')}, 'C-003': {'N2': ('not_found', None), 'N3': ('evidenced', None), 'R6': (None, 'not_found'), 'N1': ('partial', None), 'R1': ('evidenced', 'partial'), 'R2': ('evidenced', 'not_found')}, 'C-004': {'N2': ('evidenced', None), 'N3': ('evidenced', None), 'R6': (None, 'evidenced'), 'N1': ('partial', None), 'R5': ('partial', 'evidenced'), 'R2': ('evidenced', 'partial')}, 'C-005': {'N2': ('not_found', None), 'N3': ('not_found', None), 'R6': (None, 'not_found'), 'N1': ('partial', None), 'R5': ('not_found', 'evidenced'), 'R1': ('evidenced', 'partial')}, 'C-006': {'N2': ('not_found', None), 'N3': ('evidenced', None), 'R6': (None, 'not_found'), 'N1': ('not_found', None), 'R5': ('partial', 'not_found'), 'R2': ('evidenced', 'not_found')}, 'C-007': {'N2': ('not_found', None), 'N3': ('not_found', None), 'R4': ('evidenced', 'not_found'), 'R6': (None, 'partial'), 'N1': ('not_found', None), 'R2': ('evidenced', 'not_found')}, 'C-008': {'N2': ('partial', None), 'N3': ('not_found', None), 'R4': ('evidenced', 'partial'), 'R6': (None, 'not_found'), 'N1': ('not_found', None), 'R5': ('not_found', 'partial'), 'R1': ('partial', 'not_found'), 'R2': ('evidenced', 'not_found')}, 'C-009': {'N2': ('not_found', None), 'N3': ('not_found', None), 'R6': (None, 'not_found'), 'N1': ('not_found', None), 'R1': ('partial', 'not_found'), 'R2': ('partial', 'not_found')}}
- No candidate file was rewritten or copied; JD-2 reuses the same raw records via --pool-from. This is the README 'Out of scope: re-using an old pool for a new opening' item, now shown.

Logs: `lab-reports/LAB-20261121-233110ICT-s2-offline/logs`
