"""Additive patch: "Plain view" lens over docs/index.html.

Plain view (default) hides engineering detail (hashes, file paths, CLI commands)
and pins short plain-language notes next to the parts that matter, in the
case-file style of the deck (pinned paper notes, a hand-drawn START HERE ring).
Engineer view (#lens=eng) shows the page exactly as before, without notes.

No data is changed. Existing view functions are untouched: notes are added after
each render by decorate(). Fonts (OFL) are embedded so the page stays offline.

Idempotent. Usage: python3 site/add_plain_view.py
Fonts: Permanent Marker 400 and Caveat 700 (latin), SIL Open Font License.
"""
from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "index.html"
FONTS = ROOT / "site" / "fonts"


def b64(name: str) -> str:
    return base64.b64encode((FONTS / name).read_bytes()).decode()


CSS = """
@font-face{font-family:"PM";src:url(data:font/woff2;base64,__PM__) format("woff2");font-display:swap}
@font-face{font-family:"CV";src:url(data:font/woff2;base64,__CV__) format("woff2");font-weight:700;font-display:swap}
nav{flex-wrap:wrap;align-items:flex-end}
.lens{margin-left:auto;display:flex;align-items:center;gap:6px;padding-bottom:6px}
.lens .hint{font-family:"CV",cursive;font-weight:700;font-size:17px;color:#a3342a;margin-right:4px}
.lens a{font-size:12.5px;padding:5px 11px;border-radius:999px;border:1px solid var(--line);color:var(--muted);text-decoration:none;background:#fff}
.lens a.on{background:var(--ink);border-color:var(--ink);color:#f4f1ea}
body.plain .envpath, body.plain .badge:not(.strong), body.plain .prov, body.plain .gate > .small.muted,
body.plain .cand div > .pill:first-child, body.plain td.h, body.plain th.hh{display:none}
body.plain .storepre pre{max-height:460px}
.pin{position:relative;font-family:"CV",cursive;font-weight:700;font-size:19px;line-height:1.25;color:#2b2416;
  background:#f9eb9b;padding:16px 18px 13px;margin:4px 0 16px;border-radius:2px;max-width:640px;
  box-shadow:0 1px 1px rgba(0,0,0,.08),0 6px 14px -6px rgba(60,40,10,.35);transform:rotate(-.7deg)}
.pin.r{transform:rotate(.6deg)}
.pin.paper{background:#fffdf6}
.pin::before{content:"";position:absolute;top:-7px;left:50%;width:14px;height:14px;margin-left:-7px;border-radius:50%;
  background:radial-gradient(circle at 35% 35%,#ff8a7a,#c4291c 55%,#7d130b);box-shadow:0 2px 3px rgba(0,0,0,.35)}
.pin b{font-family:"PM",cursive;font-weight:400;font-size:14px;letter-spacing:.04em;color:#a3342a;display:block;margin-bottom:4px}
.pin a{color:#a3342a}
.pin.wide{max-width:none}
.sh{position:relative}
.sh-top{margin-top:38px !important}
.sh-bottom .sh-tag{top:auto;bottom:-40px;right:auto;left:12px;transform:rotate(-3deg)}
body.plain td.h ~ td, body.plain th.hh ~ th{width:auto}
body.plain table:has(td.h){width:auto;min-width:300px}
body.plain table:has(td.h) td, body.plain table:has(td.h) th{padding-right:28px}
.sh-ring{position:absolute;inset:-12px -14px;width:calc(100% + 28px);height:calc(100% + 24px);pointer-events:none;overflow:visible}
.sh-ring path{fill:none;stroke:#c4291c;stroke-width:2.6;stroke-linecap:round;vector-effect:non-scaling-stroke}
.sh-tag{position:absolute;top:-34px;right:4px;font-family:"PM",cursive;font-size:16px;color:#c4291c;transform:rotate(3deg);
  white-space:nowrap;pointer-events:none}
@media (max-width:700px){.lens{margin-left:0;width:100%;padding-top:6px}.pin{font-size:18px}}
"""

JS = r"""
function lensOf(){ return new URLSearchParams(location.hash.slice(1)).get("lens") === "eng" ? "eng" : "plain"; }
const RING = '<svg class="sh-ring" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M52,3 C83,2 99,21 98,50 C97,81 76,98 47,97 C19,96 2,79 3,49 C4,21 23,5 57,7"/></svg>';
function pin(html, cls){ const d = document.createElement("div"); d.className = "pin " + (cls||""); d.innerHTML = html; return d; }
function before(el, html, cls){ if (el) el.insertAdjacentElement("beforebegin", pin(html, cls)); }
function inside(el, html, cls){ if (el) el.insertAdjacentElement("afterbegin", pin(html, cls)); }
function startHere(el, pos){ if (!el) return; pos = pos || "top"; el.classList.add("sh", "sh-" + pos); el.insertAdjacentHTML("beforeend", RING + (pos === "none" ? "" : `<span class="sh-tag">${pos === "bottom" ? "START HERE ↖" : "START HERE ↙"}</span>`)); }
function tab(v, label){ return `<a href="${link({view:v})}">${label}</a>`; }

const NOTES = {
  screen(app){
    app.insertAdjacentElement("afterbegin", pin(`<b>CASE FILE · TALENT PRE-SCREEN</b>One job, nine synthetic candidates. The AI reads every CV and points to the lines that match the job. It does not score, rank or decide. A person does. Then see ${tab("swap","Model swap")} and ${tab("handoff","Handoff")}.`, "wide"));
    const q = app.querySelector(".grid > .card:last-child .ev blockquote");
    before(q && q.closest(".ev"), `Every line in grey is copied word for word from the CV. The ✓ means a machine checked it against the file. No ✓, no trust.`, "r");
    startHere(q);
    const gate = app.querySelector(".gate");
    before(gate, `The AI stops here. A Nestlé person presses one of these buttons. Not the model.`);
    const list = app.querySelector(".grid > .card:nth-child(2)");
    inside(list, `Sorted by ID, not by merit. There is no score to sort by.`, "paper r");
    const runs = app.querySelector(".runs");
    before(runs, `Two models, two vendors. Switch between them: the files underneath stay the same.`, "paper");
  },
  swap(app){
    app.insertAdjacentElement("afterbegin", pin(`<b>REPLACE THE AI · KEEP WHAT IT LEARNED</b>Same job, same CVs, two models from two vendors. Each writes in its own folder. Neither can edit the original files.`, "wide"));
    const t = app.querySelector("table");
    before(t, `"same file" on every row: both AIs read the exact same CVs, and nobody changed them. Click a candidate to compare the two readings below.`, "r");
    startHere(t);
    const two = app.querySelector(".two");
    before(two, `Where the two models disagree (evidenced vs partial), a person sees both side by side and decides.`);
  },
  handoff(app){
    const note = app.querySelector(".grid > .card:nth-child(2)");
    before(app.querySelector(".grid"), `The first AI stopped after five and left a note in the Store. The second AI, from another vendor, read it, skipped what was done and finished the last four. A shift handover, for machines.`, "wide r");
    startHere(note, "bottom");
    const last = app.querySelector(".two > .card:last-child");
    inside(last, `The second AI only wrote in its own folder. The first AI's files are exactly as they were.`, "paper");
  },
  live(app){
    const card = app.querySelector(".card");
    inside(card, `<b>TRY IT</b>Press the dark button. It replays a recorded run right here in your browser and re-checks every quote. No key, no network. Pick "prompt-injection test" to watch a CV try to give the AI orders.`, "wide r");
    startHere(card && [...card.querySelectorAll("button")].find(b => /simulated/.test(b.textContent)), "none");
  },
  store(app){
    const tree = app.querySelector(".tree");
    inside(tree, `<b>THIS IS THE STORE</b><u>raw</u>: the original files, locked.<br><u>curated</u>: each AI keeps its own folder.<br><u>decisions</u>: written by people, never overwritten.`, "r");
    const panel = tree && tree.nextElementSibling;
    if (panel){ panel.classList.add("storepre"); inside(panel, `What an AI wrote, exactly as it sits in the Store. Plain text with labelled fields, so the next agent, from any vendor, can read it.`, "paper"); }
  },
};

function decorate(s){
  const lens = lensOf();
  document.body.classList.toggle("plain", lens === "plain");
  const nav = $("#nav");
  nav.insertAdjacentHTML("beforeend", `<span class="lens">${lens==="plain"?'<span class="hint">all the raw detail →</span>':""}<a class="${lens==="plain"?"on":""}" href="${link({lens:""})}">Plain view</a><a class="${lens==="eng"?"on":""}" href="${link({lens:"eng"})}">Engineer view</a></span>`);
  document.querySelectorAll("#app table").forEach(t => {
    const row = [...t.rows].find(r => r.querySelector("td.h")); if (!row) return;
    [...row.cells].forEach((c, i) => { if (c.classList.contains("h") && t.rows[0].cells[i]) t.rows[0].cells[i].classList.add("hh"); });
  });
  if (lens === "plain" && NOTES[s.view]) NOTES[s.view]($("#app"));
}
"""

START, END = "/*__PLAIN_VIEW_START__*/", "/*__PLAIN_VIEW_END__*/"
CSS_START, CSS_END = "/*__PLAIN_CSS_START__*/", "/*__PLAIN_CSS_END__*/"


def put(html: str, start: str, end: str, body: str, anchor: str) -> str:
    block = f"{start}\n{body}\n{end}\n"
    if start in html:
        return re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n", lambda _: block, html, flags=re.S)
    assert html.count(anchor) == 1, anchor
    return html.replace(anchor, block + anchor)


def main() -> None:
    html = PAGE.read_text(encoding="utf-8")
    css = CSS.replace("__PM__", b64("permanent-marker-400.woff2")).replace("__CV__", b64("Caveat-700-latin.woff2"))
    html = put(html, CSS_START, CSS_END, css, "</style>\n</head>")
    html = put(html, START, END, JS, "function render(){")
    edits = [
        ('file: p.get("file") || "", hc: p.get("hc") || ""};',
         'file: p.get("file") || "", hc: p.get("hc") || "", lens: p.get("lens") || ""};'),
    ]
    for old, new in edits:
        if new in html:
            continue
        assert html.count(old) == 1, old
        html = html.replace(old, new)
    # call decorate() at the end of render()
    if "  decorate(s);\n}" not in html:
        old = "screenView(s);\n}\naddEventListener"
        assert html.count(old) == 1
        html = html.replace(old, "screenView(s);\n  decorate(s);\n}\naddEventListener")
    PAGE.write_text(html, encoding="utf-8")
    print("patched", PAGE)


if __name__ == "__main__":
    main()
