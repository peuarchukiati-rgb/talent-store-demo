"""Shared helpers for the talent-store-demo test lab.

Every suite builds a FRESH copy of the committed store under
lab/work/<run_id>/store (gitignored) and runs the engine against it via
TSD_STORE_ROOT, so the committed store/ is never touched. Reports are written
to lab-reports/<run_id>/ per the handoff's section 4 schema.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "lab" / "work"
REPORTS = (ROOT / "lab-reports").resolve()
FIXTURES = ROOT / "lab" / "fixtures"

# Fixed clock for offline mode -> byte-identical output. 2026-11-22T00:00:00Z.
LAB_EPOCH = "1795305600"
ICT = timezone(timedelta(hours=7))

# Values scrubbed from any text written to disk (logs, reports).
_HOME = str(Path.home())
_USER = os.environ.get("USER") or os.environ.get("LOGNAME") or ""
_SECRET_ENVS = ("AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "GEMINI_API_KEY",
                "OPENAI_API_KEY", "ANTHROPIC_API_KEY")


def scrub(text: str) -> str:
    """Remove home paths, usernames and any known secret env values."""
    if not text:
        return text
    out = text.replace(_HOME, "~").replace(str(ROOT), ".")
    if _USER:
        out = out.replace(_USER, "user")
    for name in _SECRET_ENVS:
        val = os.environ.get(name)
        if val and len(val) > 3:
            out = out.replace(val, f"<{name}>")
    # Redact obvious API-key shapes only (sk-..., Google AIza...). Deliberately
    # narrow so it never touches git SHAs, run_ids or ordinary hashes.
    out = re.sub(r"\bsk-[A-Za-z0-9_\-]{16,}\b", "<redacted-key>", out)
    out = re.sub(r"\bAIza[A-Za-z0-9_\-]{30,}\b", "<redacted-key>", out)
    return out


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def git_commit() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()


def dirty_tree() -> bool:
    """True if the tree has changes OUTSIDE the lab's own generated output.

    The lab writes under lab-reports/ (its reports) and lab/work/ (gitignored
    scratch); those are the lab doing its job, not a dirty source tree. We ignore
    them so a report's dirty_tree flag reflects real uncommitted source changes.
    """
    out = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    ignore = ("lab-reports/", "lab/work/", ".venv-demo/")
    dirty = []
    for line in out.splitlines():
        path = line[3:].strip().strip('"')
        # Handle rename "old -> new" by checking the destination.
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path and not path.startswith(ignore):
            dirty.append(line)
    return bool(dirty)


def now_ict_stamp() -> str:
    return datetime.now(ICT).strftime("%Y-%m-%d %H:%M:%S ICT")


def run_id(suite: str, mode: str) -> str:
    stamp = datetime.now(ICT).strftime("%Y%m%d-%H%M%S")
    return f"LAB-{stamp}ICT-{suite}-{mode}"


def fresh_store(work_id: str) -> Path:
    """A writable copy of the committed store at lab/work/<work_id>/store."""
    dest = WORK / work_id / "store"
    if dest.parent.exists():
        shutil.rmtree(dest.parent)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "store", dest)
    for p in dest.rglob("*"):
        if p.is_file():
            os.chmod(p, 0o644)
    return dest


def add_raw(store_path: Path, fixture: Path, kind: str) -> Path:
    """Copy a fixture into the lab store's raw layer. kind in {jd, candidates}.

    Caller must re-seal (cli seal) afterwards so verify passes on the lab copy.
    """
    dest = store_path / "raw" / kind / Path(fixture).name
    shutil.copy2(fixture, dest)
    os.chmod(dest, 0o644)
    return dest


def cli(args: list[str], store_path: Path, offline: bool = True,
        extra_env: dict | None = None) -> subprocess.CompletedProcess:
    """Invoke cli.py against a lab store copy. Offline sets the fixed clock."""
    env = dict(os.environ)
    env["TSD_STORE_ROOT"] = str(store_path)
    if offline:
        env["SOURCE_DATE_EPOCH"] = LAB_EPOCH
    if extra_env:
        env.update(extra_env)
    return subprocess.run([sys.executable, str(ROOT / "cli.py"), *args],
                          cwd=ROOT, env=env, capture_output=True, text=True)


def hash_dir_md(base: Path) -> dict:
    """Map of relpath -> sha256 for every .md under base (sorted)."""
    base = Path(base)
    return {p.relative_to(base).as_posix(): sha256_file(p)
            for p in sorted(base.rglob("*.md")) if p.is_file()}


class Report:
    """Accumulates one run and writes report.md + report.json + SUMMARY rows."""

    def __init__(self, rid: str, suite: str, mode: str, models: list[dict]):
        self.rid = rid
        self.suite = suite
        self.mode = mode
        self.models = models
        self.timestamp_ict = now_ict_stamp()
        self.git_commit = git_commit()
        self.dirty_tree = dirty_tree()
        self.inputs: list[dict] = []
        self.outputs: list[dict] = []
        self.assertions: list[dict] = []
        self.notes: list[str] = []
        self.dir = REPORTS / rid
        self.logs_dir = self.dir / "logs"

    def add_input(self, path, sha=None):
        p = Path(path)
        self.inputs.append({"path": rel_repo(p), "sha256": sha or sha256_file(p)})

    def add_output(self, path, sha=None):
        p = Path(path)
        self.outputs.append({"path": rel_repo(p), "sha256": sha or sha256_file(p)})

    def assert_(self, aid: str, desc: str, expected, actual, status: str):
        assert status in ("PASS", "FAIL", "NOT RUN"), status
        self.assertions.append({"id": aid, "desc": desc, "expected": str(expected),
                                "actual": str(actual), "status": status})
        return status

    def note(self, text: str):
        self.notes.append(text)

    def write_log(self, name: str, text: str):
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        (self.logs_dir / name).write_text(scrub(text), encoding="utf-8")

    @property
    def counts(self):
        c = {"PASS": 0, "FAIL": 0, "NOT RUN": 0}
        for a in self.assertions:
            c[a["status"]] += 1
        return c

    def save(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        data = {
            "run_id": self.rid, "timestamp_ict": self.timestamp_ict,
            "git_commit": self.git_commit, "dirty_tree": self.dirty_tree,
            "mode": self.mode, "suite": self.suite, "models": self.models,
            "inputs": self.inputs, "outputs": self.outputs,
            "assertions": self.assertions,
            "logs": rel_repo(self.logs_dir) if self.logs_dir.exists() else None,
            "notes": self.notes,
            "counts": self.counts,
        }
        (self.dir / "report.json").write_text(
            scrub(json.dumps(data, indent=2, ensure_ascii=False)) + "\n", encoding="utf-8")
        (self.dir / "report.md").write_text(scrub(self._md(data)), encoding="utf-8")
        _append_summary(data)
        return self.dir

    def _md(self, d: dict) -> str:
        L = [f"# Lab report · {d['run_id']}", "",
             f"- suite: **{d['suite']}**", f"- mode: **{d['mode']}**",
             f"- timestamp_ict: {d['timestamp_ict']}",
             f"- git_commit: `{d['git_commit']}`", f"- dirty_tree: {d['dirty_tree']}",
             f"- models: " + ", ".join(f"{m.get('provider')}/{m.get('model')}"
                                       f"{' ' + m['version'] if m.get('version') else ''}"
                                       for m in d["models"]), ""]
        c = d["counts"]
        L += [f"**Result: {c['PASS']} PASS · {c['FAIL']} FAIL · {c['NOT RUN']} NOT RUN**", "",
              "## Assertions", "",
              "| id | description | expected | actual | status |",
              "|----|-------------|----------|--------|--------|"]
        for a in d["assertions"]:
            L.append(f"| {a['id']} | {a['desc']} | {_cell(a['expected'])} | "
                     f"{_cell(a['actual'])} | **{a['status']}** |")
        L += ["", "## Inputs", ""]
        for i in d["inputs"]:
            L.append(f"- `{i['path']}` — `{i['sha256']}`")
        L += ["", "## Outputs", ""]
        for o in d["outputs"]:
            L.append(f"- `{o['path']}` — `{o['sha256']}`")
        if d["notes"]:
            L += ["", "## Notes", ""] + [f"- {n}" for n in d["notes"]]
        L += ["", f"Logs: `{d['logs']}`" if d["logs"] else "", ""]
        return "\n".join(L)


def _cell(s: str) -> str:
    s = str(s).replace("|", "\\|").replace("\n", " ")
    return s if len(s) <= 90 else s[:87] + "..."


def add_store_raw_inputs(rep: "Report"):
    """Record the committed raw layer (JD + candidate source files) as inputs.

    Every suite reads these same immutable records from store/raw; listing their
    paths + sha256 lets a reviewer trace each run back to the exact source bytes.
    """
    base = ROOT / "store" / "raw"
    for p in sorted(base.rglob("*.md")):
        rep.add_input(p)


def rel_repo(path) -> str:
    p = Path(path).resolve()
    try:
        return p.relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def _append_summary(data: dict):
    REPORTS.mkdir(parents=True, exist_ok=True)
    jpath = REPORTS / "SUMMARY.json"
    rows = []
    if jpath.exists():
        rows = json.loads(jpath.read_text(encoding="utf-8"))
    rows = [r for r in rows if r["run_id"] != data["run_id"]]
    c = data["counts"]
    rows.append({
        "run_id": data["run_id"], "suite": data["suite"], "mode": data["mode"],
        "models": "+".join(f"{m.get('provider')}/{m.get('model')}" for m in data["models"]),
        "pass": c["PASS"], "fail": c["FAIL"], "not_run": c["NOT RUN"],
        "git_commit": data["git_commit"], "timestamp_ict": data["timestamp_ict"],
        "report": f"lab-reports/{data['run_id']}/report.md",
    })
    rows.sort(key=lambda r: (r["suite"], r["mode"], r["run_id"]))
    jpath.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_summary_md(rows)


def _write_summary_md(rows: list[dict]):
    L = ["# Lab SUMMARY — talent-store-demo test lab", "",
         "One row per run. FAIL and NOT RUN are shown, never hidden.", "",
         "**Scope / honesty:** all data is synthetic; runs are on a single local "
         "machine with the named models. **Access control (tenant identity, "
         "role-based permissions) is OUT OF SCOPE** here — it is a Nestlé-side "
         "deployment concern, not tested by this lab.", "",
         "| run_id | suite | mode | models | PASS | FAIL | NOT RUN | commit | report |",
         "|--------|-------|------|--------|------|------|---------|--------|--------|"]
    for r in rows:
        flag = " ⚠" if r["fail"] else ""
        L.append(f"| {r['run_id']} | {r['suite']} | {r['mode']} | {r['models']} | "
                 f"{r['pass']} | {r['fail']}{flag} | {r['not_run']} | "
                 f"`{r['git_commit'][:10]}` | [report]({r['report']}) |")
    totals = {"pass": sum(r["pass"] for r in rows), "fail": sum(r["fail"] for r in rows),
              "not_run": sum(r["not_run"] for r in rows)}
    L += ["", f"**Totals:** {totals['pass']} PASS · {totals['fail']} FAIL · "
          f"{totals['not_run']} NOT RUN across {len(rows)} run(s).", ""]
    (REPORTS / "SUMMARY.md").write_text("\n".join(L), encoding="utf-8")
