#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON:-python3}"
OFFLINE_MODE=0

for arg in "$@"; do
  case "$arg" in
    --venv)
      if [[ ! -d ".venv" ]]; then
        "$PYTHON_BIN" -m venv .venv
      fi
      PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
      ;;
    --offline)
      OFFLINE_MODE=1
      ;;
    *)
      echo "Unknown option: $arg" >&2
      echo "Usage: ./setup.sh [--venv] [--offline]" >&2
      exit 2
      ;;
  esac
done

echo "Using Python: $PYTHON_BIN"
if [[ "$OFFLINE_MODE" -eq 1 ]]; then
  "$PYTHON_BIN" -m pip install --no-build-isolation --no-deps -e .
else
  "$PYTHON_BIN" -m pip install -e .
fi
echo "Setup complete. Run './run.sh' or 'make test'."
