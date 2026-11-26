# loader.py: JSON config file loader and saver (Attempt 4)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

import json
from pathlib import Path

from .validator import DEFAULT_CONFIG, ConfigValidationError, validate_config
from copy import deepcopy


def get_default_config():
    return deepcopy(DEFAULT_CONFIG)


def load_config(path):
    """Load a JSON configuration file, validate it, and return normalized config dict."""
    cfg_path = Path(path)
    if not cfg_path.exists():
        raise ConfigValidationError(f"Configuration file not found: {cfg_path}")
    try:
        text = cfg_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigValidationError(f"Could not read configuration file '{cfg_path}': {exc}") from exc

    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ConfigValidationError(
            f"Malformed JSON in '{cfg_path}' at line {exc.lineno}, column {exc.colno}: {exc.msg}"
        ) from exc

    return validate_config(raw)


def save_config(config_data, path):
    """Validate and serialize a configuration dict to a formatted JSON file."""
    normalized = validate_config(config_data)
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
    return out_path
