# Lab SUMMARY — talent-store-demo test lab

One row per run. FAIL and NOT RUN are shown, never hidden.

**Scope / honesty:** all data is synthetic; runs are on a single local machine with the named models. **Access control (tenant identity, role-based permissions) is OUT OF SCOPE** here — it is a Nestlé-side deployment concern, not tested by this lab.

| run_id | suite | mode | models | PASS | FAIL | NOT RUN | commit | report |
|--------|-------|------|--------|------|------|---------|--------|--------|
| LAB-20261121-233109ICT-s1-offline | s1 | offline | stub/stub-v1 | 5 | 0 | 1 | `4b97508772` | [report](lab-reports/LAB-20261121-233109ICT-s1-offline/report.md) |
| LAB-20261121-211920ICT-s1-real | s1 | real | codex_cli/gpt-5.6-sol+claude_cli/sonnet | 12 | 0 | 2 | `8c26f6a6a0` | [report](lab-reports/LAB-20261121-211920ICT-s1-real/report.md) |
| LAB-20261121-233110ICT-s2-offline | s2 | offline | stub/stub-v1 | 5 | 0 | 0 | `4b97508772` | [report](lab-reports/LAB-20261121-233110ICT-s2-offline/report.md) |
| LAB-20261121-233110ICT-s3-offline | s3 | offline | stub/stub-v1 | 5 | 0 | 0 | `4b97508772` | [report](lab-reports/LAB-20261121-233110ICT-s3-offline/report.md) |
| LAB-20261121-212441ICT-s3-real | s3 | real | codex_cli/gpt-5.6-sol+claude_cli/sonnet | 9 | 1 ⚠ | 0 | `8c26f6a6a0` | [report](lab-reports/LAB-20261121-212441ICT-s3-real/report.md) |
| LAB-20261121-233436ICT-s3-real-scoped | s3 | real-scoped | codex_cli/gpt-5.6-sol+claude_cli/sonnet | 8 | 2 ⚠ | 0 | `efd6748c07` | [report](lab-reports/LAB-20261121-233436ICT-s3-real-scoped/report.md) |
| LAB-20261121-233110ICT-s4-offline | s4 | offline | stub/stub-v1 | 6 | 0 | 0 | `4b97508772` | [report](lab-reports/LAB-20261121-233110ICT-s4-offline/report.md) |
| LAB-20261121-233110ICT-s5-offline | s5 | offline | stub/stub-v1 | 3 | 0 | 0 | `4b97508772` | [report](lab-reports/LAB-20261121-233110ICT-s5-offline/report.md) |

**Totals:** 53 PASS · 3 FAIL · 3 NOT RUN across 8 run(s).
