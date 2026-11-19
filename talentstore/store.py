"""The store: Markdown files with YAML frontmatter, owned by the organisation.

Layout
  store/raw/        immutable source records (JD, candidate profiles). Never rewritten.
  store/curated/    machine-written layer. One folder per run; a run never touches another run.
  store/decisions/  human decisions. Append-only log per candidate.
  store/MANIFEST.md hashes of every raw file, written once at seal time.

Any model reads from raw and writes only to curated/<run_id>/. Swapping the
model means a new run folder; raw and earlier runs stay byte-identical.
"""
from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "store"
RAW = STORE / "raw"
CURATED = STORE / "curated"
DECISIONS = STORE / "decisions"
MANIFEST = STORE / "MANIFEST.md"

_FM = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def read_md(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    m = _FM.match(text)
    if not m:
        raise ValueError(f"{path} has no frontmatter")
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def write_md(path: Path, meta: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    path.write_text(f"---\n{fm}\n---\n\n{body.strip()}\n", encoding="utf-8")


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_files() -> list[Path]:
    return sorted(p for p in RAW.rglob("*.md"))


def hash_tree(base: Path) -> dict[str, str]:
    return {rel(p): sha256(p) for p in sorted(base.rglob("*")) if p.is_file()}


def load_jd(jd_id: str) -> tuple[Path, dict, str]:
    path = RAW / "jd" / f"{jd_id}.md"
    meta, body = read_md(path)
    return path, meta, body


def load_candidates(jd_id: str) -> list[tuple[Path, dict, str]]:
    """Candidates for a JD, internal pool first (grouping only; no ordering by merit)."""
    out = []
    for p in sorted((RAW / "candidates").glob("*.md")):
        meta, body = read_md(p)
        if meta.get("applied_for") == jd_id:
            out.append((p, meta, body))
    out.sort(key=lambda t: (0 if t[1].get("pool") == "internal" else 1, t[1]["id"]))
    return out


# --- raw immutability -------------------------------------------------------

def seal_raw() -> dict[str, str]:
    """Record raw hashes in MANIFEST.md and make raw files read-only."""
    hashes = {rel(p): sha256(p) for p in raw_files()}
    lines = ["# Store manifest", "", "Raw layer hashes, written at seal time. Raw is immutable.", ""]
    lines += [f"- `{k}` sha256:{v}" for k, v in hashes.items()]
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    for p in raw_files():
        os.chmod(p, 0o444)
    return hashes


def manifest_hashes() -> dict[str, str]:
    if not MANIFEST.exists():
        return {}
    pat = re.compile(r"^- `(.+?)` sha256:([0-9a-f]{64})$")
    out = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        m = pat.match(line)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def verify_raw() -> list[str]:
    """Return a list of problems; empty means raw matches the manifest."""
    expected = manifest_hashes()
    if not expected:
        return ["MANIFEST.md missing: run `python3 seal_store.py` first"]
    actual = {rel(p): sha256(p) for p in raw_files()}
    problems = []
    for k, v in expected.items():
        if k not in actual:
            problems.append(f"missing raw file: {k}")
        elif actual[k] != v:
            problems.append(f"raw file changed: {k}")
    for k in actual.keys() - expected.keys():
        problems.append(f"raw file not in manifest: {k}")
    return problems
