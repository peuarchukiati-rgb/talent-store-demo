#!/usr/bin/env python3
"""talent-store-demo CLI.

  python3 cli.py seal                         hash raw layer into store/MANIFEST.md, make raw read-only
  python3 cli.py verify                       check raw layer against the manifest
  python3 cli.py prescreen --model gemini     run the pre-screen with a model profile from config/models.json
  python3 cli.py decide C-004 advance --by "TA: Hiring Manager" --note "..."   record a human decision
  python3 cli.py hashes                       print sha256 of every store file (for before/after proof)
  python3 cli.py render                       build site/index.html from the store
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from talentstore import prescreen, store  # noqa: E402

DECISIONS = {"advance", "hold", "decline"}


def cmd_decide(a):
    path = store.DECISIONS / f"{a.candidate}.md"
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entry = f"- {now} · **{a.decision}** · by {a.by} · on JD {a.jd} · basis: {a.run or 'latest summary'}" + \
            (f" · note: {a.note}" if a.note else "")
    if path.exists():
        meta, body = store.read_md(path)
        meta["latest"] = a.decision
        meta["updated_utc"] = now
        body = body.rstrip() + "\n" + entry
    else:
        meta = {"type": "decision_log", "candidate": a.candidate,
                "candidate_ref": f"store/raw/candidates/{a.candidate}.md", "jd": a.jd,
                "latest": a.decision, "updated_utc": now, "append_only": True}
        body = f"# Decisions · {a.candidate}\n\nHuman decisions only. Entries are appended, never edited.\n\n{entry}"
    store.write_md(path, meta, body)
    print(f"recorded: {a.candidate} → {a.decision} ({store.rel(path)})")


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seal")
    sub.add_parser("verify")
    sub.add_parser("hashes")
    sub.add_parser("render")
    ps = sub.add_parser("prescreen")
    ps.add_argument("--model", required=True)
    ps.add_argument("--jd", default="JD-SC-014")
    ps.add_argument("--config", default=str(store.ROOT / "config" / "models.json"))
    ps.add_argument("--run-id")
    ps.add_argument("--candidates", help="comma-separated subset, e.g. C-001,C-002 (only these are processed)")
    ps.add_argument("--handoff", help="after the run, write a handoff file here (done + next lists)")
    ps.add_argument("--resume", help="read a handoff file and process only its 'next' list, skipping 'done'")
    d = sub.add_parser("decide")
    d.add_argument("candidate")
    d.add_argument("decision", choices=sorted(DECISIONS))
    d.add_argument("--by", required=True)
    d.add_argument("--jd", default="JD-SC-014")
    d.add_argument("--run")
    d.add_argument("--note")
    a = p.parse_args()

    if a.cmd == "seal":
        h = store.seal_raw()
        print(f"sealed {len(h)} raw files → {store.rel(store.MANIFEST)}")
    elif a.cmd == "verify":
        problems = store.verify_raw()
        print("raw layer OK: matches manifest" if not problems else "\n".join(problems))
        sys.exit(1 if problems else 0)
    elif a.cmd == "hashes":
        for k, v in store.hash_tree(store.STORE).items():
            print(f"{v}  {k}")
    elif a.cmd == "prescreen":
        cand_list = a.candidates.split(",") if a.candidates else None
        prescreen.run(a.jd, a.model, a.config, a.run_id,
                      candidates=cand_list, handoff_out=a.handoff, resume=a.resume)
    elif a.cmd == "decide":
        cmd_decide(a)
    elif a.cmd == "render":
        from talentstore import render
        out = render.build()
        print(f"wrote {store.rel(out)}")


if __name__ == "__main__":
    main()
