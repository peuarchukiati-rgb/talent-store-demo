"""Pre-screen: evidence summary per candidate against the JD. No score, no rank.

The model gets one JD and one candidate profile from the raw layer and must
return, for each requirement, the evidence it found (quoted verbatim from the
profile) or that it found none. Quotes are checked against the source text
after the call; a quote that is not in the profile is flagged, not trusted.
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from . import providers
from .store import (CURATED, MANIFEST, load_candidates, load_jd, read_md, rel,
                    sha256, verify_raw, write_md)

SYSTEM = """You are a recruitment pre-screen assistant working for a hiring team.
You compare ONE candidate profile with ONE job description and report evidence.

Rules:
- For each requirement id, set status to exactly one of: "evidenced", "partial", "not_found".
- Every evidence item must be an exact, verbatim quote copied from the candidate profile (max 25 words). Never paraphrase inside "quote".
- The profile may be written in a language other than English (for example Vietnamese). Quote it in its original language, with every diacritic exactly as written. Never translate inside "quote".
- Write "note", "open_points" and "summary" in English, whatever the language of the profile.
- Do not score, rate, rank, compare with other candidates, or recommend hire / reject / shortlist.
- Do not infer or mention age, gender, marital status, health, religion, ethnicity or nationality.
- "open_points" are factual gaps the recruiter may want to verify, phrased neutrally.
- "summary" is 2-3 neutral sentences describing what the profile shows. No verdict words (strong, weak, ideal, best, fit, unfit).
- Output JSON only, matching this shape:
{"requirements":[{"id":"R1","status":"evidenced|partial|not_found","evidence":[{"quote":"..."}],"note":"one short sentence"}],
 "open_points":["..."],
 "summary":"..."}"""

STATUSES = {"evidenced", "partial", "not_found"}
BANNED = re.compile(r"\b(rank|ranked|ranking|best candidate|ideal|unfit|top candidate|strong fit|weak fit|recommend(ed)? (to )?(hire|reject|shortlist)|out of 10|/10)\b", re.I)


def _user_prompt(jd_meta: dict, jd_body: str, cand_body: str) -> str:
    reqs = "\n".join(f"- {r['id']} ({r['kind']}): {r['text']}" for r in jd_meta["requirements"])
    return (
        f"JOB DESCRIPTION: {jd_meta['title']} ({jd_meta['id']})\n{jd_body.strip()}\n\n"
        f"REQUIREMENTS:\n{reqs}\n\n"
        f"CANDIDATE PROFILE (quote only from this text):\n<<<\n{cand_body.strip()}\n>>>"
    )


def _parse(text: str) -> dict:
    start = text.find("{")
    if start < 0:
        raise ValueError("model returned no JSON object")
    obj, _ = json.JSONDecoder().raw_decode(text[start:])
    return obj


def _norm(s: str) -> str:
    """Comparison form for the verbatim check.

    NFC first: Vietnamese tone marks can arrive composed (U+1EC7) or decomposed
    (e + U+0323 + U+0302) depending on the source app; both must compare equal.
    """
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("–", "-")).strip().strip('"').lower()


def _check(result: dict, jd_meta: dict, source_text: str) -> list[str]:
    """Validate shape, verify quotes against the source, and flag verdict language."""
    warnings = []
    src = _norm(source_text)
    ids = {r["id"] for r in jd_meta["requirements"]}
    got = {r.get("id") for r in result.get("requirements", [])}
    if ids - got:
        warnings.append(f"missing requirements: {sorted(ids - got)}")
    for r in result.get("requirements", []):
        if r.get("status") not in STATUSES:
            warnings.append(f"{r.get('id')}: invalid status {r.get('status')!r}")
        for ev in r.get("evidence", []) or []:
            q = _norm(ev.get("quote", "")).rstrip(".")
            ev["verified"] = bool(q) and q in src
            if not ev["verified"]:
                warnings.append(f"{r.get('id')}: quote not found verbatim in profile")
    free_text = " ".join([result.get("summary", "")] + list(result.get("open_points", []))
                         + [r.get("note", "") for r in result.get("requirements", [])])
    if BANNED.search(free_text):
        warnings.append(f"verdict language detected: {BANNED.search(free_text).group(0)!r}")
    return warnings


def _render_body(cand_meta: dict, jd_meta: dict, result: dict) -> str:
    texts = {r["id"]: r for r in jd_meta["requirements"]}
    lines = [f"# Evidence summary · {cand_meta['display_name']} · {jd_meta['title']}", "",
             "> Pre-screen output. Evidence only: no score, no rank, no recommendation. A person decides.", "",
             "## Summary", "", result.get("summary", "").strip(), "", "## Evidence by requirement", ""]
    for r in result.get("requirements", []):
        req = texts.get(r.get("id"), {})
        lines.append(f"### {r.get('id')} · {req.get('kind', '')} · `{r.get('status')}`")
        lines.append(f"_{req.get('text', '')}_")
        lines.append("")
        for ev in r.get("evidence", []) or []:
            mark = "✓ verbatim" if ev.get("verified") else "⚠ not found in source"
            lines.append(f"> \"{ev.get('quote', '').strip().lstrip('#').strip()}\" — {mark}")
        if r.get("note"):
            lines.append("")
            lines.append(r["note"])
        lines.append("")
    if result.get("open_points"):
        lines += ["## Open points to verify", ""] + [f"- {p}" for p in result["open_points"]] + [""]
    return "\n".join(lines)


def _read_handoff(path: Path) -> dict:
    meta, _ = read_md(path)
    if meta.get("type") != "handoff":
        raise SystemExit(f"{rel(path)} is not a handoff file (type={meta.get('type')!r})")
    return meta


def _write_handoff(path: Path, run_id: str, runtime_label: str, jd_id: str,
                   done_entries: list[dict], next_ids: list[str]) -> Path:
    meta = {
        "type": "handoff",
        "run_a_id": run_id,
        "runtime_a": runtime_label,
        "jd": jd_id,
        "done": done_entries,
        "next": next_ids,
        "store_raw_manifest_sha": sha256(MANIFEST),
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    body = (
        f"# Handoff {path.stem} · pre-screen continuation\n\n"
        f"Run A ({runtime_label}, `{run_id}`) completed {len(done_entries)} candidate(s) for {jd_id}.\n"
        f"A later run continues the `next` list below; it must skip everything in `done`.\n"
        f"The raw store is byte-identical: `store/MANIFEST.md` sha256 is pinned above.\n"
    )
    write_md(path, meta, body)
    return path


def run(jd_id: str, profile_name: str, config_path: str, run_id: str | None = None,
        candidates: list[str] | None = None, handoff_out: str | None = None,
        resume: str | None = None, log=print) -> Path:
    problems = verify_raw()
    if problems:
        raise SystemExit("refusing to run, raw layer does not match manifest:\n  " + "\n  ".join(problems))

    cfg = providers.load_config(config_path)
    profile = cfg["profiles"][profile_name]
    model_id = profile.get("model") or profile.get("deployment")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_id = run_id or f"{stamp}-{profile_name}"
    out_dir = CURATED / run_id
    if out_dir.exists():
        raise SystemExit(f"run folder exists, refusing to overwrite: {rel(out_dir)}")

    jd_path, jd_meta, jd_body = load_jd(jd_id)
    all_cands = load_candidates(jd_id)
    all_ids = [c[1]["id"] for c in all_cands]

    # Decide the subset this run will process.
    subset_ids: list[str] | None = None
    if resume:
        hpath = Path(resume)
        if not hpath.is_absolute():
            hpath = MANIFEST.parent.parent / resume
        handoff = _read_handoff(hpath)
        done_ids = [d["id"] if isinstance(d, dict) else d for d in handoff.get("done", [])]
        next_ids = list(handoff.get("next", []))
        log(f"resume from {rel(hpath)}: run A = {handoff.get('runtime_a')} ({handoff.get('run_a_id')})")
        log(f"  SKIP (already done by run A, per handoff): {done_ids or '(none)'}")
        log(f"  CONTINUE (this run): {next_ids or '(none)'}")
        subset_ids = next_ids
    elif candidates:
        subset_ids = [c.strip() for c in candidates if c.strip()]
        log(f"subset requested: {subset_ids}")

    if subset_ids is not None:
        unknown = [c for c in subset_ids if c not in all_ids]
        if unknown:
            raise SystemExit(f"unknown candidate id(s) for {jd_id}: {unknown}")
        cands = [c for c in all_cands if c[1]["id"] in subset_ids]
    else:
        cands = all_cands

    log(f"run {run_id}: {profile['label']} ({model_id}) · {jd_id} · {len(cands)} candidate(s)")

    done_entries: list[dict] = []
    for cand_path, cand_meta, cand_body in cands:
        t0 = time.time()
        raw_text = providers.call(profile, SYSTEM, _user_prompt(jd_meta, jd_body, cand_body))
        result = _parse(raw_text)
        warnings = _check(result, jd_meta, cand_body)
        meta = {
            "type": "evidence_summary",
            "candidate": cand_meta["id"],
            "candidate_ref": rel(cand_path),
            "candidate_sha256": sha256(cand_path),
            "jd": jd_id,
            "jd_ref": rel(jd_path),
            "jd_sha256": sha256(jd_path),
            "pool": cand_meta.get("pool"),
            "run_id": run_id,
            "provider": profile["provider"],
            "model": model_id,
            "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "status": "proposed",
            "decided_by": None,
            "scored": False,
            "ranked": False,
            "checks": {"quotes_total": sum(len(r.get("evidence") or []) for r in result.get("requirements", [])),
                       "quotes_verified": sum(1 for r in result.get("requirements", [])
                                              for e in (r.get("evidence") or []) if e.get("verified")),
                       "warnings": warnings},
            "summary": result.get("summary", ""),
            "evidence": result.get("requirements", []),
            "open_points": result.get("open_points", []),
        }
        cand_out = out_dir / f"{cand_meta['id']}.md"
        write_md(cand_out, meta, _render_body(cand_meta, jd_meta, result))
        done_entries.append({"id": cand_meta["id"], "curated": rel(cand_out), "sha256": sha256(cand_out)})
        flag = f" · {len(warnings)} warning(s)" if warnings else ""
        log(f"  {cand_meta['id']} [{cand_meta.get('pool')}] {time.time() - t0:.1f}s{flag}")

    if handoff_out:
        next_ids = [i for i in all_ids if i not in {d["id"] for d in done_entries}]
        hpath = Path(handoff_out)
        if not hpath.is_absolute():
            hpath = MANIFEST.parent.parent / handoff_out
        _write_handoff(hpath, run_id, profile["label"], jd_id, done_entries, next_ids)
        log(f"handoff written: {rel(hpath)} · done={[d['id'] for d in done_entries]} · next={next_ids}")

    problems = verify_raw()
    log("raw layer after run: " + ("unchanged (matches manifest)" if not problems else "CHANGED: " + "; ".join(problems)))
    return out_dir
