"""Suite 2 — Reuse: a second JD screened against the SAME pool, no re-ingest.

A new synthetic JD (Demand Planning Analyst, JD-DP-021) is added to a lab store
copy. The existing 9-candidate pool is screened against it with --pool-from, so
no candidate file is rewritten or copied. We prove: every candidate file is
byte-identical before and after, JD-1 outputs are untouched, JD-2 outputs point
back to the same candidate_sha256, and the status map differs between JD-1 and
JD-2 (the same memory answering a new question).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lablib as L  # noqa: E402
import yaml  # noqa: E402

CANDS = [f"C-00{i}" for i in range(1, 10)]


def _status_map(path: Path) -> dict:
    meta = yaml.safe_load(path.read_text().split("\n---")[0].lstrip("-\n"))
    return {e["id"]: e["status"] for e in meta.get("evidence", [])}


def _cand_sha(path: Path) -> str:
    meta = yaml.safe_load(path.read_text().split("\n---")[0].lstrip("-\n"))
    return meta.get("candidate_sha256")


def run(mode: str) -> L.Report:
    offline = mode == "offline"
    suite = "s2"
    rid = L.run_id(suite, mode)
    prof = "stub" if offline else "claude"
    models = ([{"provider": "stub", "model": "stub-v1"}] if offline
              else [{"provider": "claude_cli", "model": "sonnet"}])
    rep = L.Report(rid, suite, mode, models)

    store = L.fresh_store(rid)
    for f in (store / "raw").rglob("*.md"):
        os.chmod(f, 0o644)

    cand_dir = store / "raw" / "candidates"
    before = L.hash_dir_md(cand_dir)

    # Run 1: JD-SC-014 (the original opening).
    r1 = L.cli(["prescreen", "--model", prof, "--jd", "JD-SC-014", "--run-id", "JD1"],
               store, offline=offline)
    rep.write_log("run-jd1.log", r1.stdout + "\n--STDERR--\n" + r1.stderr)

    # Add the SECOND JD to the lab store's raw layer and re-seal (lab copy only).
    L.add_raw(store, L.FIXTURES / "JD-DP-021.md", "jd")
    rseal = L.cli(["seal"], store, offline=offline)
    rep.write_log("reseal.log", rseal.stdout + "\n--STDERR--\n" + rseal.stderr)

    jd1_before = L.hash_dir_md(store / "curated" / "JD1")

    # Run 2: screen the SAME pool (applied_for JD-SC-014) against JD-DP-021.
    r2 = L.cli(["prescreen", "--model", prof, "--jd", "JD-DP-021",
                "--pool-from", "JD-SC-014", "--run-id", "JD2"], store, offline=offline)
    rep.write_log("run-jd2.log", r2.stdout + "\n--STDERR--\n" + r2.stderr)

    after = L.hash_dir_md(cand_dir)
    jd1_after = L.hash_dir_md(store / "curated" / "JD1")

    rep.add_input(L.FIXTURES / "JD-DP-021.md")
    for p in sorted((store / "curated" / "JD2").glob("*.md")):
        rep.add_output(p)

    rep.assert_("s2.runs", "both screening runs exit 0", "rc 0 and rc 0",
                f"jd1={r1.returncode} jd2={r2.returncode}",
                "PASS" if r1.returncode == 0 == r2.returncode else "FAIL")

    unchanged = before == after
    changed_files = [k for k in before if before.get(k) != after.get(k)]
    rep.assert_("s2.candidates_identical",
                "every candidate file sha256 identical before vs after (no re-ingest)",
                "all 9 identical", "all identical" if unchanged else f"changed: {changed_files}",
                "PASS" if unchanged and len(before) == 9 else "FAIL")

    jd1_untouched = jd1_before == jd1_after and bool(jd1_before)
    rep.assert_("s2.jd1_untouched", "JD-1 outputs are byte-identical after the JD-2 run",
                "unchanged", "unchanged" if jd1_untouched else "CHANGED",
                "PASS" if jd1_untouched else "FAIL")

    # JD-2 outputs point back to the same candidate_sha256 as the raw files.
    ref_ok, ref_detail = True, []
    for cid in CANDS:
        jd2 = store / "curated" / "JD2" / f"{cid}.md"
        raw = cand_dir / f"{cid}.md"
        if jd2.exists():
            got, want = _cand_sha(jd2), L.sha256_file(raw)
            if got != want:
                ref_ok = False
                ref_detail.append(f"{cid}:{got[:8]}!={want[:8]}")
    rep.assert_("s2.ref_back", "JD-2 outputs carry the raw candidate_sha256 (traceable to source)",
                "all match raw file hash", "all match" if ref_ok else ";".join(ref_detail),
                "PASS" if ref_ok else "FAIL")

    # Status differs between JD-1 and JD-2 for at least one candidate.
    diffs = {}
    for cid in CANDS:
        f1 = store / "curated" / "JD1" / f"{cid}.md"
        f2 = store / "curated" / "JD2" / f"{cid}.md"
        if f1.exists() and f2.exists():
            m1, m2 = _status_map(f1), _status_map(f2)
            d = {k: (m1.get(k), m2.get(k)) for k in set(m1) | set(m2) if m1.get(k) != m2.get(k)}
            if d:
                diffs[cid] = d
    rep.assert_("s2.new_question", "same pool yields a DIFFERENT status map for the new JD",
                ">=1 candidate differs JD-1 vs JD-2", f"{len(diffs)} candidate(s) differ",
                "PASS" if diffs else "FAIL")
    rep.note(f"Per-candidate status diff JD-1(JD-SC-014) vs JD-2(JD-DP-021): {diffs}")
    rep.note("No candidate file was rewritten or copied; JD-2 reuses the same raw records "
             "via --pool-from. This is the README 'Out of scope: re-using an old pool for a "
             "new opening' item, now shown.")
    if not offline:
        rep.note("Real mode: statuses reflect Claude Sonnet's reading, not byte-stable.")
    return rep


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "offline"
    r = run(m)
    r.save()
    c = r.counts
    print(f"{r.rid}: {c['PASS']} PASS {c['FAIL']} FAIL {c['NOT RUN']} NOT RUN")
    sys.exit(1 if c["FAIL"] else 0)
