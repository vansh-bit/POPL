#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON:-python3}"

if [[ "${1:-}" == "--venv" ]]; then
  if [[ ! -d ".venv" ]]; then
    "$PYTHON_BIN" -m venv .venv
  fi
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
fi

echo "Using Python: $PYTHON_BIN"
"$PYTHON_BIN" -m pip install --no-build-isolation --no-deps -e .
echo "Setup complete. Run './run.sh' or 'make test'."
