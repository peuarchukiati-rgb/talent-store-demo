"""Additive patch: add a read-only "Handoff" tab to docs/index.html.

Shows the 2026-11-21 continuation run (continuation-evidence/): run A (OpenAI GPT-5.6)
pre-screened C-001..C-005 and wrote store/handoffs/H-001.md; run B (Claude Sonnet)
resumed from it and did C-006..C-009. Existing data (D) and tabs are not touched;
the continuation data is embedded as a separate CONT object.

Idempotent: re-running replaces the previously injected block.
Usage: python3 site/add_handoff_view.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from talentstore.store import read_md, sha256, verify_raw  # noqa: E402

PAGE = ROOT / "docs" / "index.html"
S = ROOT / "store"

# Expected hashes, copied from continuation-evidence/hash-table.md (recorded 2026-11-21).
EXPECT = {
    "store/handoffs/H-001.md": "7a5f9a2a2510bfed0b92a1ed104fb317c6c4630a4dbb46d327f2990cafa32273",
    "store/MANIFEST.md": "cacbc5e8120fae367d506e737d8de9a3d94b17637b95cb228df08b01bee3ab00",
    "store/curated/A-openai/C-001.md": "8e7b2c24a0f7142014f812da927d6e18e28db11966fdf1cb3644a5fd050411c8",
    "store/curated/A-openai/C-002.md": "09618841818d0bdbc3ab6498d45c40ddb7f16bba41a050d3bd5c8a30edb1f531",
    "store/curated/A-openai/C-003.md": "a6ce4515985903fd55a61bfe16e527271c4fb12b43ab49b2f1513e2419029c41",
    "store/curated/A-openai/C-004.md": "0c40aac0053b51fee2e6a631bd23202bc78935530af7b30e19e9cf7a6dfb60a1",
    "store/curated/A-openai/C-005.md": "1b1615b39fb502100b234d631085612ac95d6ecb8c5c414cef20af6763078259",
    "store/curated/B-claude/C-006.md": "5481e0f62d3bc0dfed8f73dcc43006762db69354e3e267e93f15f05b4947216c",
    "store/curated/B-claude/C-007.md": "2ce8b40b1924cf39ee4f75ab86f09b1c08560b1d3eb0fb68667a331fbe013116",
    "store/curated/B-claude/C-008.md": "b116cad41eee5b2d93fda31d1853c1954abe958eba7bc9a3d0ca2f3692f14212",
    "store/curated/B-claude/C-009.md": "9113654f478ed58bf5561dc82b3f6596a274c8bd3a44581e4796da4af488377f",
}


def run(folder: str, label: str, model_label: str) -> dict:
    out = {"id": folder, "label": label, "model_label": model_label, "summaries": {}}
    for f in sorted((S / "curated" / folder).glob("*.md")):
        meta, _ = read_md(f)
        out["summaries"][meta["candidate"]] = {"meta": meta, "ref": f"store/curated/{folder}/{f.name}"}
    return out


def snapshot() -> dict:
    for ref, want in EXPECT.items():
        got = sha256(ROOT / ref)
        if got != want:
            sys.exit(f"hash mismatch, refusing to build: {ref} {got} != {want}")
    h_meta, h_body = read_md(S / "handoffs" / "H-001.md")
    cands = {}
    for f in sorted((S / "raw" / "candidates").glob("C-*.md")):
        m, _ = read_md(f)
        cands[m["id"]] = {"display_name": m["display_name"], "current_role": m["current_role"],
                          "pool": m["pool"], "source_ref": m["source_ref"]}
    return {
        "handoff": {"meta": h_meta, "body": h_body.strip(), "ref": "store/handoffs/H-001.md",
                    "sha256": EXPECT["store/handoffs/H-001.md"]},
        "a": run("A-openai", "Run A", "OpenAI GPT-5.6"),
        "b": run("B-claude", "Run B", "Anthropic Claude Sonnet"),
        "cands": cands,
        "manifest_sha": EXPECT["store/MANIFEST.md"],
        "a_files": {k: v for k, v in EXPECT.items() if "/A-openai/" in k},
        "raw_ok_now": not verify_raw(),
        "date": "2026-11-21",
    }


JS = r"""
function handoffView(s){
  const C = CONT, A = C.a, B = C.b, H = C.handoff.meta;
  const all = {...A.summaries, ...B.summaries};
  const cur = all[s.hc] ? s.hc : "C-009";
  const sum = all[cur], who = A.summaries[cur] ? A : B, c = C.cands[cur] || {};
  const m = sum.meta;
  const chip = (run, id) => `<a class="cand ${id===cur?"on":""}" href="${link({view:"handoff", hc:id})}" style="padding:8px 10px"><div class="nm">${esc(id)} · ${esc(C.cands[id]?.display_name)}</div><div class="meta">quotes ${run.summaries[id].meta.checks.quotes_verified}/${run.summaries[id].meta.checks.quotes_total} verified</div></a>`;
  const aRows = Object.entries(C.a_files).map(([f,h]) => `<tr><td>${esc(f.split("/").pop())}</td><td class="h">${short(h)}</td><td class="h">${short(h)}</td><td class="same">same file</td></tr>`).join("");
  return `<div class="banner ${C.raw_ok_now?"":"bad"}">${C.raw_ok_now?"✓ Raw store unchanged before run A, after run A and after run B: store/MANIFEST.md @ "+short(C.manifest_sha):"⚠ Raw store does not match manifest"}</div>
  <div class="card" style="margin-bottom:16px">
    <h2>Swap the AI mid-run · the work carries on</h2>
    <div class="small">${esc(C.date)} · one JD, nine synthetic candidates, two runtimes, one handoff note. Run A stopped after five candidates and wrote a handoff into the store. Run B, a different model from a different vendor, read that note, skipped what was done and finished the rest. It wrote only its own folder.</div>
  </div>
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(260px,1fr));margin-bottom:16px">
    <div class="card"><h2>1 · ${esc(A.label)} · ${esc(A.model_label)}</h2><div class="muted small" style="margin-bottom:8px">store/curated/${esc(A.id)}/ · done</div>${Object.keys(A.summaries).map(id=>chip(A,id)).join("")}</div>
    <div class="card" style="background:var(--accent-soft)"><h2>Handoff note · H-001</h2>
      <div class="small" style="font-family:ui-monospace,Menlo,monospace;line-height:1.7">type: ${esc(H.type)}<br>runtime_a: ${esc(H.runtime_a)}<br>jd: ${esc(H.jd)}<br>done: ${esc((H.done||[]).map(x=>x.id).join(", "))}<br>next: ${esc((H.next||[]).join(", "))}<br>raw manifest: ${short(H.store_raw_manifest_sha)}</div>
      <p class="small" style="margin-top:10px"><i>"A later run continues the next list below; it must skip everything in done."</i></p>
      <div class="muted small">${esc(C.handoff.ref)} @ ${short(C.handoff.sha256)}</div></div>
    <div class="card"><h2>2 · ${esc(B.label)} · ${esc(B.model_label)}</h2><div class="muted small" style="margin-bottom:8px">store/curated/${esc(B.id)}/ · resumed from H-001</div>${Object.keys(B.summaries).map(id=>chip(B,id)).join("")}</div>
  </div>
  <div class="two" style="margin-bottom:16px">
    <div class="card">
      <h2>Evidence summary · ${esc(who.label)} · ${esc(who.model_label)}</h2>
      <h3>${esc(c.display_name)} <span class="pill ${c.pool==="internal"?"int":""}">${esc(c.pool)}</span></h3>
      <div class="muted small">${esc(c.current_role)} · source: ${esc(c.source_ref)}</div>
      <p style="margin:12px 0 4px">${esc(m.summary)}</p>
      ${evidenceBlock(sum)}
      <div class="prov">file: ${esc(sum.ref)}<br>model: ${esc(m.model)} via ${esc(m.provider)} · ${esc(m.created_utc)}<br>reads: ${esc(m.candidate_ref)} @ ${short(m.candidate_sha256)}<br>quotes verified: ${m.checks.quotes_verified}/${m.checks.quotes_total} · scored: ${m.scored} · ranked: ${m.ranked} · decided_by: ${esc(m.decided_by ?? "null")}</div>
    </div>
    <div class="card">
      <h2>Run B did not touch run A</h2>
      <div class="small">Run A's five files, hashed before and after run B.</div>
      <table style="margin-top:10px"><tr><th>File</th><th>Before B</th><th>After B</th><th></th></tr>${aRows}</table>
      <div class="small muted" style="margin-top:12px">Agents propose; a person decides. Nothing here is scored or ranked.</div>
      <div class="small muted" style="margin-top:8px">The Pre-screen and Model swap tabs show a separate, earlier test: the same pre-screen on both models over eight candidates (67/67 and 61/61 quotes verified). Synthetic data only. Evidence: continuation-evidence/ in the repo.</div>
    </div>
  </div>`;
}
"""

START, END = "/*__HANDOFF_VIEW_START__*/", "/*__HANDOFF_VIEW_END__*/"


def main() -> None:
    html = PAGE.read_text(encoding="utf-8")
    data = json.dumps(snapshot(), ensure_ascii=False, default=str).replace("</", "<\\/")
    block = f"{START}\nconst CONT = {data};\n{JS}\n{END}\n"
    if START in html:
        html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", lambda _: block, html, flags=re.S)
    else:
        anchor = "function render(){"
        assert html.count(anchor) == 1
        html = html.replace(anchor, block + anchor)
    edits = [
        ('file: p.get("file") || ""};', 'file: p.get("file") || "", hc: p.get("hc") || ""};'),
        ('["live","Run live ⚡"],["store","Store files"]]', '["handoff","Handoff"],["live","Run live ⚡"],["store","Store files"]]'),
        ('s.view === "live" ? liveView(s) :', 's.view === "live" ? liveView(s) : s.view === "handoff" ? handoffView(s) :'),
    ]
    for old, new in edits:
        if new in html:
            continue
        assert html.count(old) == 1, old
        html = html.replace(old, new)
    PAGE.write_text(html, encoding="utf-8")
    print("patched", PAGE)


if __name__ == "__main__":
    main()
