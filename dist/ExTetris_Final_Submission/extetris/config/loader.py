# loader.py: JSON config file loader and saver
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from copy import deepcopy
import json
from pathlib import Path

from .validator import DEFAULT_CONFIG, ConfigValidationError, validate_config


def get_default_config():
    return deepcopy(DEFAULT_CONFIG)


def load_config(path):
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
    normalized = validate_config(config_data)
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
    return out_path
