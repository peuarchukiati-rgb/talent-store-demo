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
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
# Additive (lab): a store-root override lets the lab run every suite on a fresh
# copy under lab/work/<run_id>/ and never touch the committed store/.
# Resolved once at import time, from TSD_STORE_ROOT; default is unchanged.
_STORE_ENV = os.environ.get("TSD_STORE_ROOT")
STORE = Path(_STORE_ENV).resolve() if _STORE_ENV else ROOT / "store"
RAW = STORE / "raw"
CURATED = STORE / "curated"
DECISIONS = STORE / "decisions"
HANDOFFS = STORE / "handoffs"
MANIFEST = STORE / "MANIFEST.md"

_FM = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)

# Additive (lab): instruction-like patterns used by the optional CV injection
# check. The check RECORDS flags; it never edits or strips the source file.
_INJECTION_PATTERNS = [
    (r"ignore (the|all|any|previous|above)[\w\s]*", "override-instruction"),
    (r"disregard (the|all|any|previous|above)[\w\s]*", "override-instruction"),
    (r"rank (me|this candidate)[\w\s]*", "rank-steer"),
    (r"(mark|set|treat|rate) (all|every|each)[\w\s]*(requirement|criteria)[\w\s]*", "status-steer"),
    (r"you (must|should|will) (now|only|always)[\w\s]*", "imperative-to-model"),
    (r"as an? (ai|assistant|language model)[\w\s]*", "role-address"),
    (r"(strong fit|best candidate|top candidate|recommend[\w\s]*hire)", "verdict-steer"),
    (r"<!--.*?-->", "html-comment"),
]


def now_utc() -> datetime:
    """UTC clock, overridable for byte-identical offline output.

    Honours SOURCE_DATE_EPOCH (seconds) when set; otherwise the wall clock.
    Default behaviour (env unset) is unchanged.
    """
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if epoch:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc)
    return datetime.now(timezone.utc)


def detect_injection(text: str) -> list[dict]:
    """Flag instruction-like text in a CV. Records only; never strips.

    Returns a list of {kind, match, line} in document order. Case-insensitive.
    """
    flags: list[dict] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        low = line.lower()
        for pat, kind in _INJECTION_PATTERNS:
            m = re.search(pat, low, re.I | re.S)
            if m:
                flags.append({"kind": kind, "match": m.group(0).strip()[:80], "line": line[:120]})
    return flags


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
    rp = path.resolve()
    # Express store paths relative to the store's parent so refs stay
    # "store/..."-shaped for both the committed store and any lab copy (which
    # lives under lab/work/<run_id>/). For the default store STORE.parent == ROOT,
    # so this is byte-identical to the original ROOT-relative behaviour.
    try:
        return rp.relative_to(STORE.parent).as_posix()
    except ValueError:
        pass
    try:
        return rp.relative_to(ROOT).as_posix()
    except ValueError:
        return rp.name


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


def load_candidates(jd_id: str, pool_from: str | None = None,
                    pool_all: bool = False) -> list[tuple[Path, dict, str]]:
    """Candidates for a JD, internal pool first (grouping only; no ordering by merit).

    Additive (lab): screen an existing pool against a *different* JD without
    touching candidate files.
      pool_all=True        -> every candidate profile in the store
      pool_from="JD-SC-014" -> candidates whose applied_for is that JD
    Default (both unset) is unchanged: candidates whose applied_for == jd_id.
    """
    select = pool_from or jd_id
    out = []
    for p in sorted((RAW / "candidates").glob("*.md")):
        meta, body = read_md(p)
        if pool_all or meta.get("applied_for") == select:
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


def is_default_store() -> bool:
    """True when STORE is the committed store/ (used to guard destructive ops)."""
    return STORE.resolve() == (ROOT / "store").resolve()


def erase_candidate(cand_id: str) -> dict:
    """Erase every trace of one candidate from THIS store (lab copies only).

    Removes the raw profile, every curated summary, the decision log and any
    handoff reference, then re-seals the MANIFEST. Refuses to run on the
    committed store/. Returns a record of removed/modified files with hashes.
    """
    if is_default_store():
        raise RuntimeError(
            "refusing to erase in the committed store/. Set TSD_STORE_ROOT to a lab copy.")
    record: dict = {"candidate": cand_id, "removed": [], "modified": []}

    def _unlink(p: Path):
        if p.exists():
            record["removed"].append({"path": rel(p), "sha256_before": sha256(p)})
            p.unlink()

    _unlink(RAW / "candidates" / f"{cand_id}.md")
    if CURATED.exists():
        for run_dir in sorted(CURATED.iterdir()):
            if run_dir.is_dir():
                _unlink(run_dir / f"{cand_id}.md")
    _unlink(DECISIONS / f"{cand_id}.md")

    # Scrub handoff references (done/next lists mentioning the candidate).
    if HANDOFFS.exists():
        for hp in sorted(HANDOFFS.glob("*.md")):
            meta, body = read_md(hp)
            before = sha256(hp)
            done = [d for d in meta.get("done", [])
                    if (d.get("id") if isinstance(d, dict) else d) != cand_id]
            nxt = [c for c in meta.get("next", []) if c != cand_id]
            changed = done != meta.get("done", []) or nxt != meta.get("next", [])
            if changed:
                meta["done"], meta["next"] = done, nxt
                write_md(hp, meta, body)
                record["modified"].append(
                    {"path": rel(hp), "sha256_before": before, "sha256_after": sha256(hp)})

    # Re-seal the manifest so raw layer still verifies after removal.
    before_manifest = sha256(MANIFEST) if MANIFEST.exists() else None
    seal_raw()
    record["modified"].append(
        {"path": rel(MANIFEST), "sha256_before": before_manifest, "sha256_after": sha256(MANIFEST)})
    # Re-point every handoff's pinned manifest sha to the new manifest.
    if HANDOFFS.exists():
        new_manifest = sha256(MANIFEST)
        for hp in sorted(HANDOFFS.glob("*.md")):
            meta, body = read_md(hp)
            if meta.get("store_raw_manifest_sha") and meta["store_raw_manifest_sha"] != new_manifest:
                before = sha256(hp)
                meta["store_raw_manifest_sha"] = new_manifest
                write_md(hp, meta, body)
                record["modified"].append(
                    {"path": rel(hp), "sha256_before": before, "sha256_after": sha256(hp),
                     "field": "store_raw_manifest_sha"})
    return record


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
