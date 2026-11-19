"""Model providers. The store never depends on which one runs.

Each provider takes (system, user) text and returns the model's raw text.
Which provider and model run is decided by config/models.json, not by code.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import urllib.request


class ProviderError(RuntimeError):
    pass


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


PROVIDERS = {"azure_openai": azure_openai, "gemini": gemini, "claude_cli": claude_cli, "codex_cli": codex_cli}


def load_config(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def call(profile: dict, system: str, user: str) -> str:
    fn = PROVIDERS.get(profile["provider"])
    if fn is None:
        raise ProviderError(f"unknown provider {profile['provider']!r}")
    return fn(profile, system, user)
