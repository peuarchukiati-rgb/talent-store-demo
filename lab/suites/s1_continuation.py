"""Suite 1 — Continuation across model pairs.

Agent A screens part of the pool, is interrupted, writes a handoff. Agent B
resumes from the store + handoff ONLY (no shared memory), skips what A did, and
finishes the rest. Raw stays byte-identical; A's outputs are never touched by B.

Offline (stub) proves the MECHANICS deterministically (one provider, so the
'different model' and 'overlap divergence' dimensions are NOT RUN). Real mode
runs openai->claude and claude->openai with a genuine model swap plus an overlap.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lablib as L  # noqa: E402

RAW_AGG_PIN = "3bb695fe3b39e165b2b0f43467c90bc1c703122ce6932453144fa98e8843f2bc"
ALL = ["C-001", "C-002", "C-003", "C-004", "C-005", "C-006", "C-007", "C-008", "C-009"]
A_FIRST = ["C-001", "C-002", "C-003", "C-004", "C-005"]
B_REST = ["C-006", "C-007", "C-008", "C-009"]


def _raw_agg(store: Path) -> str:
    import hashlib
    hs = [L.sha256_file(p) for p in sorted((store / "raw").rglob("*.md"))]
    return hashlib.sha256("".join(hs).encode()).hexdigest()


def _pair(rep: L.Report, store: Path, a_profile: str, b_profile: str,
          offline: bool, tag: str):
    """One direction A(a_profile) -> B(b_profile). Returns dict of results."""
    raw_before = _raw_agg(store)
    # A screens the first five, interrupted, writes a handoff.
    ra = L.cli(["prescreen", "--model", a_profile, "--jd", "JD-SC-014",
                "--run-id", f"A-{tag}", "--candidates", ",".join(A_FIRST),
                "--handoff", f"H-{tag}.md"], store, offline=offline)
    rep.write_log(f"{tag}-runA.log", ra.stdout + "\n--STDERR--\n" + ra.stderr)
    a_dir = store / "curated" / f"A-{tag}"
    a_hashes_before = L.hash_dir_md(a_dir) if a_dir.exists() else {}
    raw_after_a = _raw_agg(store)
    # B resumes from the handoff alone.
    rb = L.cli(["prescreen", "--model", b_profile, "--jd", "JD-SC-014",
                "--run-id", f"B-{tag}", "--resume", f"H-{tag}.md"], store, offline=offline)
    rep.write_log(f"{tag}-runB.log", rb.stdout + "\n--STDERR--\n" + rb.stderr)
    b_dir = store / "curated" / f"B-{tag}"
    a_hashes_after = L.hash_dir_md(a_dir) if a_dir.exists() else {}
    raw_after_b = _raw_agg(store)
    a_ids = sorted(p.stem for p in a_dir.glob("*.md")) if a_dir.exists() else []
    b_ids = sorted(p.stem for p in b_dir.glob("*.md")) if b_dir.exists() else []
    return {
        "ok_a": ra.returncode == 0, "ok_b": rb.returncode == 0,
        "raw_before": raw_before, "raw_after_a": raw_after_a, "raw_after_b": raw_after_b,
        "a_hashes_before": a_hashes_before, "a_hashes_after": a_hashes_after,
        "a_ids": a_ids, "b_ids": b_ids, "a_dir": a_dir, "b_dir": b_dir,
    }


def run(mode: str) -> L.Report:
    offline = mode == "offline"
    suite = "s1"
    rid = L.run_id(suite, mode)
    if offline:
        models = [{"provider": "stub", "model": "stub-v1"}]
    else:
        models = [{"provider": "codex_cli", "model": "gpt-5.6-sol", "version": cli_ver("codex")},
                  {"provider": "claude_cli", "model": "sonnet", "version": cli_ver("claude")}]
    rep = L.Report(rid, suite, mode, models)

    directions = ([("stub", "stub", "stub")] if offline
                  else [("openai", "claude", "oc"), ("claude", "openai", "co")])

    for a_prof, b_prof, tag in directions:
        store = L.fresh_store(f"{rid}-{tag}")
        for f in (store / "raw").rglob("*.md"):
            import os
            os.chmod(f, 0o644)
        res = _pair(rep, store, a_prof, b_prof, offline, tag)
        pre = f"[{a_prof}->{b_prof}]"
        for p in sorted(res["a_dir"].glob("*.md")) + sorted(res["b_dir"].glob("*.md")):
            rep.add_output(p)

        rep.assert_(f"{tag}.runs", f"{pre} both runs exit 0",
                    "A ok and B ok", f"A={res['ok_a']} B={res['ok_b']}",
                    "PASS" if res["ok_a"] and res["ok_b"] else "FAIL")
        rep.assert_(f"{tag}.raw_pin", f"{pre} raw aggregate matches the pinned value throughout",
                    RAW_AGG_PIN,
                    f"before={res['raw_before'][:12]} afterA={res['raw_after_a'][:12]} "
                    f"afterB={res['raw_after_b'][:12]}",
                    "PASS" if res["raw_before"] == res["raw_after_a"] == res["raw_after_b"] == RAW_AGG_PIN
                    else "FAIL")
        rep.assert_(f"{tag}.b_skips_done", f"{pre} B processed only the handoff 'next' list",
                    B_REST, res["b_ids"], "PASS" if res["b_ids"] == B_REST else "FAIL")
        rep.assert_(f"{tag}.a_untouched", f"{pre} A's outputs are byte-identical after B ran",
                    "all A files unchanged",
                    "unchanged" if res["a_hashes_before"] == res["a_hashes_after"] and res["a_hashes_before"]
                    else "CHANGED/empty",
                    "PASS" if res["a_hashes_before"] == res["a_hashes_after"] and res["a_hashes_before"]
                    else "FAIL")
        union = res["a_ids"] + res["b_ids"]
        rep.assert_(f"{tag}.coverage", f"{pre} all 9 candidates covered exactly once (A + B)",
                    "9 unique, no overlap", f"{len(union)} ids, {len(set(union))} unique",
                    "PASS" if sorted(union) == ALL and len(union) == 9 else "FAIL")

    # Overlap + model-divergence dimension.
    if offline:
        rep.assert_("overlap.divergence",
                    "overlap: same candidate through two DIFFERENT models, status diff",
                    "status diff reported", "only the stub provider exists offline",
                    "NOT RUN")
        rep.note("Offline uses the deterministic stub for both A and B, so A and B are the "
                 "SAME engine. The continuation MECHANICS (raw unchanged, skip done, A untouched, "
                 "exact coverage) are proven here; the model-difference and overlap-divergence "
                 "dimensions require real mode (openai<->claude).")
    else:
        _overlap(rep)
    rep.note(f"Swap granularity: the handoff boundary is a whole candidate; A did {A_FIRST}, "
             f"B did {B_REST}. No candidate is split across models.")
    return rep


def _overlap(rep: L.Report):
    """Real mode: run C-001 and C-007 through BOTH models; report status diffs."""
    store = L.fresh_store(f"{rep.rid}-overlap")
    import os
    for f in (store / "raw").rglob("*.md"):
        os.chmod(f, 0o644)
    ids = ["C-001", "C-007"]
    diffs = {}
    for prof in ("openai", "claude"):
        r = L.cli(["prescreen", "--model", prof, "--jd", "JD-SC-014",
                   "--run-id", f"OV-{prof}", "--candidates", ",".join(ids)], store, offline=False)
        rep.write_log(f"overlap-{prof}.log", r.stdout + "\n--STDERR--\n" + r.stderr)
    import yaml
    for cid in ids:
        per = {}
        for prof in ("openai", "claude"):
            f = store / "curated" / f"OV-{prof}" / f"{cid}.md"
            if f.exists():
                meta = yaml.safe_load(f.read_text().split("\n---")[0].lstrip("-\n"))
                per[prof] = {e["id"]: e["status"] for e in meta.get("evidence", [])}
        diffs[cid] = per
        if "openai" in per and "claude" in per:
            changed = {k: (per["openai"].get(k), per["claude"].get(k))
                       for k in set(per["openai"]) | set(per["claude"])
                       if per["openai"].get(k) != per["claude"].get(k)}
            rep.assert_(f"overlap.{cid}",
                        f"overlap {cid}: per-requirement status reported for both models",
                        "both models produce a status map",
                        f"diffs={changed or 'none'}",
                        "PASS" if per["openai"] and per["claude"] else "FAIL")
        else:
            rep.assert_(f"overlap.{cid}", f"overlap {cid}: both models ran",
                        "both ran", f"got {list(per)}", "FAIL")
    rep.note(f"Overlap status maps (synthetic, two real models): {diffs}")


def cli_ver(name: str) -> str:
    import subprocess, shutil, os
    exe = shutil.which(name)
    if not exe and name == "codex":
        cand = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"
        exe = cand if os.path.exists(cand) else None
    if not exe:
        return "not found"
    try:
        r = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=30)
        return L.scrub((r.stdout or r.stderr).strip().splitlines()[0]) if (r.stdout or r.stderr) else "?"
    except Exception as e:
        return f"err:{type(e).__name__}"


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "offline"
    r = run(m)
    r.save()
    c = r.counts
    print(f"{r.rid}: {c['PASS']} PASS {c['FAIL']} FAIL {c['NOT RUN']} NOT RUN")
    sys.exit(1 if c["FAIL"] else 0)
