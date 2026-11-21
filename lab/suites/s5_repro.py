"""Suite 5 — Reproducibility.

Offline: run the full pre-screen twice from two independent fresh store copies
and prove the output hashes are identical, byte for byte. Records Python and
pyyaml versions (pin pyyaml if YAML bytes ever vary across machines).

Real: not byte-identical by design; logs provider, model alias and CLI version,
and states that real-mode outputs are expected to vary.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import lablib as L  # noqa: E402


def _run_once(tag: str, prof: str, offline: bool, rep: L.Report):
    store = L.fresh_store(tag)
    for f in (store / "raw").rglob("*.md"):
        os.chmod(f, 0o644)
    r = L.cli(["prescreen", "--model", prof, "--jd", "JD-SC-014", "--run-id", "REPRO"],
              store, offline=offline)
    rep.write_log(f"{tag}.log", r.stdout + "\n--STDERR--\n" + r.stderr)
    out = store / "curated" / "REPRO"
    return out, L.hash_dir_md(out), r.returncode


def run(mode: str) -> L.Report:
    offline = mode == "offline"
    suite = "s5"
    rid = L.run_id(suite, mode)
    prof = "stub" if offline else "claude"
    import yaml
    pyver = sys.version.split()[0]
    models = ([{"provider": "stub", "model": "stub-v1",
                "version": f"python {pyver} / pyyaml {yaml.__version__}"}] if offline
              else [{"provider": "claude_cli", "model": "sonnet"}])
    rep = L.Report(rid, suite, mode, models)
    L.add_store_raw_inputs(rep)

    if offline:
        out1, h1, rc1 = _run_once(f"{rid}-run1", prof, True, rep)
        out2, h2, rc2 = _run_once(f"{rid}-run2", prof, True, rep)
        for p in sorted(out1.glob("*.md")):
            rep.add_output(p)
        rep.assert_("s5.runs", "both repro runs exit 0", "rc 0 and 0",
                    f"{rc1},{rc2}", "PASS" if rc1 == 0 == rc2 else "FAIL")
        rep.assert_("s5.same_fileset", "both runs produce the same 9 output files",
                    "9 files, same names", f"{len(h1)} vs {len(h2)}",
                    "PASS" if set(h1) == set(h2) and len(h1) == 9 else "FAIL")
        identical = h1 == h2
        mism = [k for k in h1 if h1.get(k) != h2.get(k)]
        rep.assert_("s5.byte_identical",
                    "every output file is byte-identical across two independent runs",
                    "all sha256 equal", "all equal" if identical else f"differ: {mism}",
                    "PASS" if identical else "FAIL")
        import hashlib
        agg = hashlib.sha256("".join(h1[k] for k in sorted(h1)).encode()).hexdigest()
        rep.note(f"Deterministic offline output aggregate sha256: {agg}")
        rep.note(f"Environment: python {pyver}, pyyaml {yaml.__version__}. "
                 f"pyyaml is pinned in requirements.txt; SOURCE_DATE_EPOCH={L.LAB_EPOCH} "
                 f"(2026-11-22T00:00:00Z) fixes created_utc.")
        rep.note("A reviewer can re-run on Linux from a fresh clone and expect this same "
                 "aggregate, given the same Python minor and pyyaml versions.")
    else:
        out1, h1, rc1 = _run_once(f"{rid}-run1", prof, False, rep)
        out2, h2, rc2 = _run_once(f"{rid}-run2", prof, False, rep)
        for p in sorted(out1.glob("*.md")):
            rep.add_output(p)
        rep.assert_("s5.runs", "both real runs exit 0", "rc 0 and 0",
                    f"{rc1},{rc2}", "PASS" if rc1 == 0 == rc2 else "FAIL")
        rep.assert_("s5.real_varies",
                    "real-mode outputs are NOT expected byte-identical (model nondeterminism)",
                    "documented, not asserted equal",
                    "identical" if h1 == h2 else "varied (expected)", "PASS")
        rep.note(f"claude --version: {_ver('claude')}")
        rep.note("Real mode is logged, not pinned: provider claude_cli, model alias 'sonnet'. "
                 "Byte-identical reproduction is a property of offline mode only.")
    return rep


def _ver(name: str) -> str:
    import shutil
    exe = shutil.which(name)
    if not exe:
        return "not found"
    try:
        r = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=30)
        return L.scrub((r.stdout or r.stderr).strip().splitlines()[0])
    except Exception as e:
        return f"err:{type(e).__name__}"


if __name__ == "__main__":
    m = sys.argv[1] if len(sys.argv) > 1 else "offline"
    r = run(m)
    r.save()
    c = r.counts
    print(f"{r.rid}: {c['PASS']} PASS {c['FAIL']} FAIL {c['NOT RUN']} NOT RUN")
    sys.exit(1 if c["FAIL"] else 0)
