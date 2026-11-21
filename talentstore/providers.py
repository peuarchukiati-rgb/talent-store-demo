"""Model providers. The store never depends on which one runs.

Each provider takes (system, user) text and returns the model's raw text.
Which provider and model run is decided by config/models.json, not by code.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.request

from .store import detect_injection


class ProviderError(RuntimeError):
    pass


# --- stub provider (offline, deterministic) ---------------------------------
# No key, no CLI, no network. Output is a pure function of the input text, so
# two runs on the same inputs are byte-identical. Quotes are real substrings of
# the profile, so the verbatim check in prescreen is genuinely exercised.

_STOP = {
    "the", "and", "for", "with", "has", "have", "run", "a", "an", "of", "in",
    "or", "to", "at", "on", "least", "end", "least", "team", "data", "stated",
    "works", "only", "not", "least", "least", "level", "least", "years", "year",
}


def _keywords(text: str) -> list[str]:
    """Deterministic keyword list from a requirement sentence."""
    words = re.findall(r"[a-zA-Z&/]+", text.lower())
    seen, out = set(), []
    for w in words:
        w = w.strip("&/")
        if len(w) >= 4 and w not in _STOP and w not in seen:
            seen.add(w)
            out.append(w)
    return out


def _clean_quote(line: str, limit: int = 25) -> str:
    """A verbatim prefix of a profile line, markers stripped, <= limit words."""
    q = line.lstrip("#").lstrip("-").lstrip("*").strip()
    words = q.split()
    return " ".join(words[:limit])


def stub(cfg: dict, system: str, user: str) -> str:
    """Deterministic offline pre-screen. Mechanical keyword evidence matching.

    It is not a model: it cannot read Vietnamese or reason. Its only jobs are to
    be reproducible and to feed the verbatim/BANNED/injection checks with real,
    traceable substrings. Instruction-like lines (per the injection detector)
    are never quoted as evidence.
    """
    m = re.search(r"<<<\n(.*)\n>>>", user, re.S)
    profile = m.group(1).strip() if m else ""
    req_lines = re.findall(r"^- (\S+) \((\w+)\): (.+)$", user, re.M)

    flagged = {f["line"] for f in detect_injection(profile)}
    prof_lines = [ln.strip() for ln in profile.splitlines() if ln.strip()]
    safe_lines = [ln for ln in prof_lines if ln[:120] not in flagged]

    requirements = []
    counts = {"evidenced": 0, "partial": 0, "not_found": 0}
    for rid, _kind, rtext in req_lines:
        kws = _keywords(rtext)
        evidence, matched_kw = [], set()
        for ln in safe_lines:
            low = ln.lower()
            hit = [k for k in kws if k in low]
            if hit:
                matched_kw.update(hit)
                if len(evidence) < 2:
                    evidence.append({"quote": _clean_quote(ln)})
        if len(matched_kw) >= 2:
            status = "evidenced"
        elif len(matched_kw) == 1:
            status = "partial"
        else:
            status = "not_found"
        counts[status] += 1
        note = ("Keyword evidence located in the profile text."
                if evidence else "No matching evidence located in the profile text.")
        requirements.append({"id": rid, "status": status, "evidence": evidence, "note": note})

    open_points = [f"Verify requirement {r['id']} with the candidate."
                   for r in requirements if r["status"] != "evidenced"]
    k = len(requirements)
    summary = (f"Automated offline pre-screen over {k} requirement(s): "
               f"{counts['evidenced']} evidenced, {counts['partial']} partial, "
               f"{counts['not_found']} not_found. Evidence is quoted from the profile; a person reviews it.")
    return json.dumps({"requirements": requirements, "open_points": open_points, "summary": summary})


def _post_json(url: str, payload: dict, headers: dict, timeout: int = 180) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json", **headers}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:  # surface the API's message, never the key
        raise ProviderError(f"HTTP {e.code}: {e.read()[:300]!r}") from None


def azure_openai(cfg: dict, system: str, user: str) -> str:
    """Azure OpenAI chat completions (proposed default inside a Nestlé tenant)."""
    endpoint = os.environ.get(cfg.get("endpoint_env", "AZURE_OPENAI_ENDPOINT"))
    key = os.environ.get(cfg.get("key_env", "AZURE_OPENAI_API_KEY"))
    if not endpoint or not key:
        raise ProviderError("Azure OpenAI endpoint/key not set in environment")
    url = (
        f"{endpoint.rstrip('/')}/openai/deployments/{cfg['deployment']}/chat/completions"
        f"?api-version={cfg.get('api_version', '2024-10-21')}"
    )
    data = _post_json(
        url,
        {
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        {"api-key": key},
    )
    return data["choices"][0]["message"]["content"]


def gemini(cfg: dict, system: str, user: str) -> str:
    key = os.environ.get(cfg.get("key_env", "GEMINI_API_KEY"))
    if not key:
        raise ProviderError("GEMINI_API_KEY not set in environment")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{cfg['model']}:generateContent"
    data = _post_json(
        url,
        {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
        },
        {"x-goog-api-key": key},
    )
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise ProviderError(f"unexpected Gemini response: {str(data)[:300]}") from None


def claude_cli(cfg: dict, system: str, user: str) -> str:
    """Claude via the local Claude Code CLI, isolated: no user settings, no tools, no session saved."""
    exe = shutil.which("claude")
    if not exe:
        raise ProviderError("claude CLI not found")
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(
            [exe, "-p", "--setting-sources", "", "--model", cfg["model"], "--system-prompt", system,
             "--tools", "", "--no-session-persistence"],
            input=user, capture_output=True, text=True, cwd=tmp, timeout=300,
        )
    if r.returncode != 0:
        raise ProviderError(f"claude CLI exit {r.returncode}: {r.stderr[:300]}")
    return r.stdout


CODEX_APP_BIN = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"


def codex_cli(cfg: dict, system: str, user: str) -> str:
    """OpenAI via the local Codex CLI, isolated: ephemeral, read-only sandbox, no user config."""
    exe = shutil.which("codex") or (CODEX_APP_BIN if os.path.exists(CODEX_APP_BIN) else None)
    if not exe:
        raise ProviderError("codex CLI not found")
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "out.txt")
        r = subprocess.run(
            [exe, "exec", "--ephemeral", "--sandbox", "read-only", "--skip-git-repo-check",
             "--ignore-user-config", "--ignore-rules", "-m", cfg["model"],
             "-c", f"model_reasoning_effort={cfg.get('reasoning_effort', 'low')}", "-o", out, "-"],
            input=f"{system}\n\n{user}", capture_output=True, text=True, cwd=tmp, timeout=600,
        )
        if r.returncode != 0:
            raise ProviderError(f"codex exit {r.returncode}: {r.stderr[-300:]}")
        with open(out, encoding="utf-8") as f:
            return f.read()


PROVIDERS = {"azure_openai": azure_openai, "gemini": gemini, "claude_cli": claude_cli,
             "codex_cli": codex_cli, "stub": stub}


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def call(profile: dict, system: str, user: str) -> str:
    fn = PROVIDERS.get(profile["provider"])
    if fn is None:
        raise ProviderError(f"unknown provider {profile['provider']!r}")
    return fn(profile, system, user)
