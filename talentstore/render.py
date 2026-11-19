"""Build site/index.html: a read-only viewer over the store.

The page embeds a snapshot of the store as JSON. It never writes to the store;
human decisions are recorded with `cli.py decide` (the page shows the command).
"""
from __future__ import annotations

import json
from pathlib import Path

from .store import CURATED, DECISIONS, MANIFEST, ROOT, load_candidates, load_jd, read_md, rel, sha256, verify_raw

JD_ID = "JD-SC-014"


def _snapshot() -> dict:
    jd_path, jd_meta, jd_body = load_jd(JD_ID)
    cands = [{"meta": m, "body": b, "ref": rel(p), "sha256": sha256(p)} for p, m, b in load_candidates(JD_ID)]
    runs = []
    for d in sorted(p for p in CURATED.iterdir() if p.is_dir()) if CURATED.exists() else []:
        if d.name.startswith("test-"):
            continue
        summaries = {}
        for f in sorted(d.glob("*.md")):
            meta, _ = read_md(f)
            raw_text = f.read_text(encoding="utf-8")
            summaries[meta["candidate"]] = {"meta": meta, "ref": rel(f), "sha256": sha256(f),
                                            "frontmatter": raw_text.split("\n---", 1)[0] + "\n---"}
        if summaries:
            first = next(iter(summaries.values()))["meta"]
            runs.append({"id": d.name, "provider": first["provider"], "model": first["model"],
                         "created": first["created_utc"], "summaries": summaries})
    decisions = {}
    for f in sorted(DECISIONS.glob("*.md")) if DECISIONS.exists() else []:
        meta, body = read_md(f)
        decisions[meta["candidate"]] = {"latest": meta.get("latest"),
                                        "entries": [l[2:] for l in body.splitlines() if l.startswith("- ")]}
    return {
        "jd": {"meta": jd_meta, "body": jd_body, "ref": rel(jd_path), "sha256": sha256(jd_path)},
        "candidates": cands,
        "runs": runs,
        "decisions": decisions,
        "manifest": MANIFEST.read_text(encoding="utf-8") if MANIFEST.exists() else "",
        "raw_ok": not verify_raw(),
    }


def build() -> Path:
    data = json.dumps(_snapshot(), ensure_ascii=False, default=str).replace("</", "<\\/")
    html = (ROOT / "talentstore" / "viewer.html").read_text(encoding="utf-8").replace("/*__DATA__*/null", data)
    out = ROOT / "site" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out
