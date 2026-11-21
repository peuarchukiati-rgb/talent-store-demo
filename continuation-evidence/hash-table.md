# Hash table - raw immutability + A-untouched proof

Run date: 2026-11-21 (UTC). JD: JD-SC-014. 9 candidates, two runtimes, one handoff.

## Raw store (must be identical across all three columns)

| Artifact | Before any run | After run A | After run B |
|---|---|---|---|
| raw layer aggregate sha256 | `3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc` | `3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc` | `3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc` |
| store/MANIFEST.md sha256 | `cacbc5e8120fae367d506e737d8de9a3d94b17637b95cb228df08b01bee3ab00` | `cacbc5e8120fae367d506e737d8de9a3d94b17637b95cb228df08b01bee3ab00` | `cacbc5e8120fae367d506e737d8de9a3d94b17637b95cb228df08b01bee3ab00` |

`cli.py verify` printed **"raw layer OK: matches manifest"** before A, after A, and after B.
Raw aggregate = sha256 over the per-file sha256 of every `store/raw/**/*.md` (9 candidates + 1 JD).

## Run A curated files (must be identical before and after run B → B never touched A)

| File | sha256 before B | sha256 after B | identical |
|---|---|---|---|
| store/curated/A-openai/C-001.md | `8e7b2c24a0f7142014f812da927d6e18e28db11966fdf1cb3644a5fd050411c8` | `8e7b2c24a0f7142014f812da927d6e18e28db11966fdf1cb3644a5fd050411c8` | yes |
| store/curated/A-openai/C-002.md | `09618841818d0bdbc3ab6498d45c40ddb7f16bba41a050d3bd5c8a30edb1f531` | `09618841818d0bdbc3ab6498d45c40ddb7f16bba41a050d3bd5c8a30edb1f531` | yes |
| store/curated/A-openai/C-003.md | `a6ce4515985903fd55a61bfe16e527271c4fb12b43ab49b2f1513e2419029c41` | `a6ce4515985903fd55a61bfe16e527271c4fb12b43ab49b2f1513e2419029c41` | yes |
| store/curated/A-openai/C-004.md | `0c40aac0053b51fee2e6a631bd23202bc78935530af7b30e19e9cf7a6dfb60a1` | `0c40aac0053b51fee2e6a631bd23202bc78935530af7b30e19e9cf7a6dfb60a1` | yes |
| store/curated/A-openai/C-005.md | `1b1615b39fb502100b234d631085612ac95d6ecb8c5c414cef20af6763078259` | `1b1615b39fb502100b234d631085612ac95d6ecb8c5c414cef20af6763078259` | yes |

## Run B curated files (B wrote only its own folder, C-006..C-009)

| File | sha256 |
|---|---|
| store/curated/B-claude/C-006.md | `5481e0f62d3bc0dfed8f73dcc43006762db69354e3e267e93f15f05b4947216c` |
| store/curated/B-claude/C-007.md | `2ce8b40b1924cf39ee4f75ab86f09b1c08560b1d3eb0fb68667a331fbe013116` |
| store/curated/B-claude/C-008.md | `b116cad41eee5b2d93fda31d1853c1954abe958eba7bc9a3d0ca2f3692f14212` |
| store/curated/B-claude/C-009.md | `9113654f478ed58bf5561dc82b3f6596a274c8bd3a44581e4796da4af488377f` |

## Handoff

| Artifact | sha256 |
|---|---|
| store/handoffs/H-001.md | `7a5f9a2a2510bfed0b92a1ed104fb317c6c4630a4dbb46d327f2990cafa32273` |
