# Reproduce - sequential handoff-continuation

Repo: `~/talent-store-demo`
Branch: `main`
Local commit SHA: `the latest commit on main`
Date run: 2026-11-21 (UTC)

> The two runs below write to NEW run folders (`A-openai`, `B-claude`) and a NEW
> handoff (`store/handoffs/H-001.md`). To re-run from scratch, delete those first:
> `rm -rf store/curated/A-openai store/curated/B-claude store/handoffs/H-001.md`
> (never touch `store/raw/**` or `store/MANIFEST.md`).

## 0. Setup

```
cd ~/talent-store-demo
git checkout main
. .venv-demo/bin/activate          # deps already installed; else: python3 -m venv .venv-demo && . .venv-demo/bin/activate && pip install -q -r requirements.txt
python3 cli.py verify              # must print: raw layer OK: matches manifest
```

## 1. Run A - OpenAI GPT-5.6 (local Codex CLI), screens C-001..C-005, writes handoff

```
python3 cli.py prescreen \
  --model openai \
  --candidates C-001,C-002,C-003,C-004,C-005 \
  --run-id A-openai \
  --handoff store/handoffs/H-001.md
```

Writes `store/curated/A-openai/C-00[1-5].md` and `store/handoffs/H-001.md`.

## 2. Run B - Claude Sonnet (local Claude CLI), resumes from handoff, continues C-006..C-009

```
python3 cli.py prescreen \
  --model claude \
  --resume store/handoffs/H-001.md \
  --run-id B-claude
```

Reads H-001, skips A's `done` (C-001..C-005), processes only `next` (C-006..C-009),
writes `store/curated/B-claude/C-00[6-9].md`. Does not touch `store/curated/A-openai/`.

## 3. Confirm immutability

```
python3 cli.py verify   # raw layer OK: matches manifest (unchanged before/after both runs)
```

## Notes

- Providers are configured in `config/models.json`; profile `openai` -> `codex_cli`
  (bin `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex`), profile
  `claude` -> `claude_cli` (`claude` on PATH). No API keys are used by either; both
  run isolated/ephemeral.
- The commit also contains unrelated prior-session files in the repo tree; the
  continuation evidence itself is self-contained under `continuation-evidence/`.
- Screenshots were rendered with `continuation-evidence/render_shot.py` (needs Pillow).
```
python3 -I continuation-evidence/render_shot.py store/handoffs/H-001.md continuation-evidence/shot1-H-001.png "<title>"
python3 -I continuation-evidence/render_shot.py continuation-evidence/run-B.log continuation-evidence/shot2-B-resume-log.png "<title>"
```
