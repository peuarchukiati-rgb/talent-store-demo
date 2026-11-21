#!/usr/bin/env bash
# Entry point for the talent-store-demo test lab.
#
#   ./lab/run.sh                      all suites, offline (order: 1 2 5 3 4)
#   ./lab/run.sh --mode offline       same (explicit)
#   ./lab/run.sh --mode real          all suites, real mode (codex_cli + claude_cli)
#   ./lab/run.sh --suite 3            one suite, offline
#   ./lab/run.sh --suite 1 --mode real
#
# Offline needs no key, no CLI and no network. Real mode uses the local codex +
# claude CLIs (local CLI subscription, no API key). gemini/azure are never run here.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

MODE="offline"
SUITE="all"
PY="${PYTHON:-python3}"
# Prefer the project venv if present.
if [ -x "$ROOT/.venv-demo/bin/python3" ]; then PY="$ROOT/.venv-demo/bin/python3"; fi

while [ $# -gt 0 ]; do
  case "$1" in
    --mode) MODE="$2"; shift 2;;
    --suite) SUITE="$2"; shift 2;;
    --pair) shift 2;;              # accepted for compatibility; suites pair internally
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

ORDER="1 2 5 3 4"   # handoff priority order

suite_file() {
  case "$1" in
    1) echo s1_continuation;; 2) echo s2_reuse;; 3) echo s3_injection;;
    4) echo s4_erasure;; 5) echo s5_repro;;
    *) echo ""; return 1;;
  esac
}

run_one() {
  local n="$1" f
  f="$(suite_file "$n")" || { echo "unknown suite: $n" >&2; return 2; }
  echo "=== suite $n ($MODE) ==="
  "$PY" "$ROOT/lab/suites/${f}.py" "$MODE"
}

rc=0
if [ "$SUITE" = "all" ]; then
  for n in $ORDER; do run_one "$n" || rc=1; done
else
  run_one "$SUITE" || rc=1
fi

echo "=== lab done ($MODE). See lab-reports/SUMMARY.md ==="
exit $rc
