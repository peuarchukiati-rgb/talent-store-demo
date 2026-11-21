# Lab report · LAB-20261121-211920ICT-s1-real

- suite: **s1**
- mode: **real**
- timestamp_ict: 2026-11-21 21:19:20 ICT
- git_commit: `8c26f6a6a01d789d9746c2a5f8aae0f42f6e6d64`
- dirty_tree: True
- models: codex_cli/gpt-5.6-sol codex-cli 0.169.0-alpha.11.1, claude_cli/sonnet 2.1.327 (Claude Code)

**Result: 12 PASS · 0 FAIL · 2 NOT RUN**

## Assertions

| id | description | expected | actual | status |
|----|-------------|----------|--------|--------|
| oc.runs | [openai->claude] both runs exit 0 | A ok and B ok | A=True B=True | **PASS** |
| oc.raw_pin | [openai->claude] raw aggregate matches the pinned value throughout | 3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc | before=3bb695fe3b39 afterA=3bb695fe3b39 afterB=3bb695fe3b39 | **PASS** |
| oc.b_skips_done | [openai->claude] B processed only the handoff 'next' list | ['C-006', 'C-007', 'C-008', 'C-009'] | ['C-006', 'C-007', 'C-008', 'C-009'] | **PASS** |
| oc.a_untouched | [openai->claude] A's outputs are byte-identical after B ran | all A files unchanged | unchanged | **PASS** |
| oc.coverage | [openai->claude] all 9 candidates covered exactly once (A + B) | 9 unique, no overlap | 9 ids, 9 unique | **PASS** |
| co.runs | [claude->openai] both runs exit 0 | A ok and B ok | A=True B=True | **PASS** |
| co.raw_pin | [claude->openai] raw aggregate matches the pinned value throughout | 3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc | before=3bb695fe3b39 afterA=3bb695fe3b39 afterB=3bb695fe3b39 | **PASS** |
| co.b_skips_done | [claude->openai] B processed only the handoff 'next' list | ['C-006', 'C-007', 'C-008', 'C-009'] | ['C-006', 'C-007', 'C-008', 'C-009'] | **PASS** |
| co.a_untouched | [claude->openai] A's outputs are byte-identical after B ran | all A files unchanged | unchanged | **PASS** |
| co.coverage | [claude->openai] all 9 candidates covered exactly once (A + B) | 9 unique, no overlap | 9 ids, 9 unique | **PASS** |
| overlap.C-001 | overlap C-001: per-requirement status reported for both models | both models produce a status map | diffs={'R4': ('evidenced', 'partial'), 'R5': ('evidenced', 'partial'), 'R2': ('partial'... | **PASS** |
| overlap.C-007 | overlap C-007: per-requirement status reported for both models | both models produce a status map | diffs={'R1': ('evidenced', 'partial')} | **PASS** |
| overlap.gemini | gemini: continuation + overlap run on this pool | status maps from Google Gemini | NOT RUN — no GEMINI_API_KEY on this machine | **NOT RUN** |
| overlap.azure | azure: continuation + overlap run on this pool | status maps from Azure OpenAI | NOT RUN — no Azure tenant endpoint/key on this machine | **NOT RUN** |

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

- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-co/C-001.md` — `853301a7a26e3fc4ffc2aca66ba9ce1c3bea37f15ad581e4f8ae0538dab1cad3`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-co/C-002.md` — `e49f4e4ae2efa0cc87bb3db52f6df3d0c24121118bcf88fce70297bcde34f9fb`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-co/C-003.md` — `2cb09ac771656b5e1cd33f8543b5e8552c18006496fc51c897f8589e6ff8c03e`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-co/C-004.md` — `71c14933d1b4c87043b37e7e4b4298365cbf84aa323e5b2872b9b71b914b844e`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-co/C-005.md` — `e3b32fdb82349782b837f376f1373c6e19e3fc74a694be43b72ee18b67055eef`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-oc/C-001.md` — `742a4c75e0755de3fb2ec4b70a736d33321f43a8dec8cae6bda61d4567311b55`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-oc/C-002.md` — `e1302f74938131ed2d749c65b3ce40b38f43dc35b1b84f86bd9418be82ae919f`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-oc/C-003.md` — `2f1128d5c1a8f5459aab31cdd2b47b80b71255ad1f7272146c4a9b2966177057`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-oc/C-004.md` — `f32103c192096bcf90fb5b589e63c3af74c021869a11c95c4705899f157d694e`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/A-oc/C-005.md` — `0cd71ec930daa6095eb808eddaf798811c2e99bd2029259cc2a100119363e8a5`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-co/C-006.md` — `577b939430a9e6d1fb3dd1d5ab4ed7f89a1a1e0dd4c04b446aeafec000cd40bb`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-co/C-007.md` — `d735a8f5a7d2d18d60af7f46af46338cdf8a02db9ef17b522bc64add1a589aad`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-co/C-008.md` — `4c490174688b25a20cd2e91ef9f1be12b13f8a6f617ee69d93735ed10446c89d`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-co/C-009.md` — `07d12352d53bbfa2ebd38ade76758227891f0b3a804a0f53ef492497b665cd52`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-oc/C-006.md` — `ef2929b1ef8c9ab26c69b6247760c68a071255eb2c6c4e20eacfeffd0bd0ab70`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-oc/C-007.md` — `c27c0f5e2de6c019ad46f7f9b5696f81d745f62e008db1535cecb215f3be0223`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-oc/C-008.md` — `860e54803b9ce3ce766edc6d305d15581eff3ded972ca4b79e46c14aaa6d42e7`
- `lab-reports/LAB-20261121-211920ICT-s1-real/outputs/B-oc/C-009.md` — `fbbcf8dcff6354473bb2467a91299d6113483d457301b43333512757a20a094a`

## Notes

- Overlap status maps (synthetic, two real models): {'C-001': {'openai': {'R1': 'evidenced', 'R2': 'partial', 'R3': 'evidenced', 'R4': 'evidenced', 'R5': 'evidenced', 'N1': 'evidenced', 'N2': 'evidenced', 'N3': 'evidenced'}, 'claude': {'R1': 'evidenced', 'R2': 'evidenced', 'R3': 'evidenced', 'R4': 'partial', 'R5': 'partial', 'N1': 'evidenced', 'N2': 'evidenced', 'N3': 'evidenced'}}, 'C-007': {'openai': {'R1': 'evidenced', 'R2': 'partial', 'R3': 'partial', 'R4': 'evidenced', 'R5': 'partial', 'N1': 'not_found', 'N2': 'partial', 'N3': 'not_found'}, 'claude': {'R1': 'partial', 'R2': 'partial', 'R3': 'partial', 'R4': 'evidenced', 'R5': 'partial', 'N1': 'not_found', 'N2': 'partial', 'N3': 'not_found'}}}
- Swap granularity: the handoff boundary is a whole candidate; A did ['C-001', 'C-002', 'C-003', 'C-004', 'C-005'], B did ['C-006', 'C-007', 'C-008', 'C-009']. No candidate is split across models.
- Gemini and Azure are implemented provider adapters but were not run here (no API key / no tenant). Recorded as NOT RUN, never faked; the handoff mechanism is model-agnostic by config.

Logs: `lab-reports/LAB-20261121-211920ICT-s1-real/logs`

## Provenance
- Annotated after the run (NOT RUN rows, inputs, outputs, CLI versions); run executed at 8c26f6a, tagged `lab-real-run`; engine code (talentstore/, cli.py, config/) is byte-identical at lab-clean.
