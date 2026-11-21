"""Suite 4 — Erasure.

A lab store copy with run outputs, a handoff, a human decision and a rendered
site. We erase one candidate (C-004) and prove that the id, display name and
unique profile strings are gone from raw, curated, decisions, handoffs, MANIFEST
and the rendered site; that unrelated files keep their hashes; and we list the
files that had to change (MANIFEST re-seal, handoff done-entry) with before/after
hashes. Honest note on Git history and what production deletion would require.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lablib as L  # noqa: E402

TARGET = "C-004"
# Distinctive synthetic strings from C-004's profile (display_name + unique phrases).
NEEDLES = ["C-004", "Duc N.", "finished-goods write-offs for short shelf-life SKUs by 22%",
           "a dairy company in Long An"]
UNRELATED = ["C-001", "C-005", "C-009"]  # must keep their hashes


def _grep_store(store: Path, needle: str) -> list[str]:
    hits = []
    roots = [store, store.parent / "site"]
    for base in roots:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file():
                try:
                    if needle in p.read_text(encoding="utf-8", errors="ignore"):
                        hits.append(L.rel_repo(p))
                except Exception:
                    pass
    return hits


def run(mode: str) -> L.Report:
    offline = mode == "offline"
    suite = "s4"
    rid = L.run_id(suite, mode)
    prof = "stub" if offline else "claude"
    models = ([{"provider": "stub", "model": "stub-v1"}] if offline
              else [{"provider": "claude_cli", "model": "sonnet"}])
    rep = L.Report(rid, suite, mode, models)

    store = L.fresh_store(rid)
    for f in (store / "raw").rglob("*.md"):
        os.chmod(f, 0o644)

    # Build a realistic state: a fresh run, a decision on C-004, a rendered site.
    L.cli(["prescreen", "--model", prof, "--jd", "JD-SC-014", "--run-id", "LABRUN"],
          store, offline=offline)
    L.cli(["decide", TARGET, "advance", "--by", "TA: Hiring Manager (synthetic)",
           "--run", "LABRUN", "--note", "phone screen"], store, offline=offline)
    L.cli(["render"], store, offline=offline)

    # Snapshot before erasure.
    before = L.hash_dir_md(store)
    present_before = {n: _grep_store(store, n) for n in NEEDLES}
    rep.assert_("s4.present_before", f"{TARGET} is present across the store + site before erasure",
                "hits in raw/curated/decisions/handoffs/site",
                f"{sum(len(v) for v in present_before.values())} file-hits",
                "PASS" if all(present_before.values()) else "FAIL")

    # Erase.
    er = L.cli(["erase", TARGET], store, offline=offline)
    rep.write_log("erase.log", er.stdout + "\n--STDERR--\n" + er.stderr)
    # Re-render so the site reflects the erased store.
    L.cli(["render"], store, offline=offline)

    # Zero hits anywhere after erase + re-render.
    after_hits = {n: _grep_store(store, n) for n in NEEDLES}
    total_hits = sum(len(v) for v in after_hits.values())
    rep.assert_("s4.zero_hits",
                f"after erasure, {TARGET} id/name/unique-strings return zero hits everywhere",
                "0 hits across raw, curated, decisions, handoffs, MANIFEST, site",
                f"{total_hits} hits ({ {k: v for k, v in after_hits.items() if v} })",
                "PASS" if total_hits == 0 else "FAIL")

    # raw still verifies after the re-seal.
    v = L.cli(["verify"], store, offline=offline)
    rep.assert_("s4.verify_after", "raw layer still verifies after erasure + re-seal",
                "raw layer OK", v.stdout.strip().splitlines()[-1] if v.stdout else "no output",
                "PASS" if "raw layer OK" in v.stdout else "FAIL")

    # Unrelated files keep their hashes.
    after = L.hash_dir_md(store)
    moved = []
    for cid in UNRELATED:
        for k in before:
            if f"/{cid}.md" in k and k in after and before[k] != after[k]:
                moved.append(k)
    rep.assert_("s4.unrelated_intact", "files unrelated to the erased candidate keep their sha256",
                "no unrelated file changed", moved or "all intact",
                "PASS" if not moved else "FAIL")

    # List changed/removed files with before/after hashes.
    removed = [k for k in before if k not in after]
    changed = [k for k in before if k in after and before[k] != after[k]]
    for k in removed:
        rep.note(f"removed: {k} (was sha256:{before[k][:16]}...)")
    for k in changed:
        rep.note(f"re-written: {k} sha256 {before[k][:12]}... -> {after[k][:12]}...")
    rep.assert_("s4.changeset_bounded",
                "only the target's files are removed; only MANIFEST + handoff are re-written",
                "removed = C-004 traces; changed = MANIFEST.md + handoffs",
                f"removed {len(removed)} file(s); changed {sorted(set(Path(c).name for c in changed))}",
                "PASS" if all(TARGET in r for r in removed) and
                all(("MANIFEST" in c or "handoff" in c.lower()) for c in changed) else "FAIL")

    # Guard: erase refuses to touch the committed store.
    guard = subprocess.run([sys.executable, str(L.ROOT / "cli.py"), "erase", "C-999"],
                           cwd=L.ROOT, capture_output=True, text=True,
                           env={**os.environ, "TSD_STORE_ROOT": ""})
    refused = guard.returncode != 0 and "refusing to erase" in (guard.stderr + guard.stdout)
    rep.assert_("s4.guard_default_store", "erase refuses to run against the committed store/",
                "non-zero exit, 'refusing to erase'",
                "refused" if refused else f"rc={guard.returncode}",
                "PASS" if refused else "FAIL")

    rep.note("HONEST LIMIT — Git history: this erasure cleans the working store, but the "
             "candidate's content still exists in Git history (commit 42ff14c). The data here is "
             "synthetic, so there is no harm. Production deletion of real PII would require: no Git "
             "as the system of record for PII; deletion across the store, search indexes, backups, "
             "logs and the model provider's retention; and a deletion RECORD that itself holds no PII.")
    rep.note("Run on a lab store copy only; the committed store/ was never touched (guard enforced).")
    return rep


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "offline"
    r = run(m)
    r.save()
    c = r.counts
    print(f"{r.rid}: {c['PASS']} PASS {c['FAIL']} FAIL {c['NOT RUN']} NOT RUN")
    sys.exit(1 if c["FAIL"] else 0)
