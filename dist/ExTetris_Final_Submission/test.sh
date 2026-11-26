#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
else
  PYTHON_BIN="${PYTHON:-python3}"
fi

export PYTHONPATH="${ROOT_DIR}${PYTHONPATH:+:$PYTHONPATH}"

if "$PYTHON_BIN" -c "import pytest" >/dev/null 2>&1; then
  exec "$PYTHON_BIN" -m pytest tests -v "$@"
else
  exec "$PYTHON_BIN" -m unittest discover -s tests -t . -v "$@"
fi
