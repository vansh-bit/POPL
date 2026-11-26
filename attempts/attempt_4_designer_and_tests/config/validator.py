# validator.py: Explicit schema and semantic validator for ExTetris JSON configs (Attempt 4)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from copy import deepcopy
import json
from pathlib import Path


SCHEMA_PATH = Path(__file__).resolve().parent / "schema.json"

VALID_VARIANTS = ("classic", "extended", "chaos", "custom")
VALID_SCOPES = ("one_sided", "fixed")
VALID_CONNECTIVITIES = ("any", "orthogonal", "diagonal")
VALID_STRATEGIES = ("uniform", "weighted", "bag", "adaptive", "markov")
VALID_RENDERERS = ("headless", "cli", "tk")

DEFAULT_CONFIG = {
    "name": "ExTetris Custom Variant",
    "description": "Configurable Extended Tetris variant.",
    "variant": "extended",
    "piece_scope": "one_sided",
    "connectivity": "any",
    "max_holes": None,
    "board": {
        "width": 10,
        "height": 20,
    },
    "gameplay": {
        "initial_speed_ms": 1000,
        "speed_factor": 0.92,
        "enable_wall_kicks": True,
        "enable_ghost": True,
    },
    "distribution": {
        "strategy": "bag",
        "bag_multiplier": 1,
        "repeat_penalty": 0.1,
        "weights_by_id": {},
        "seed": None,
    },
    "renderer": "cli",
}


class ConfigValidationError(ValueError):
    """Raised with human-readable diagnostics when a game configuration is invalid."""

    def __init__(self, errors):
        if isinstance(errors, str):
            self.errors = [errors]
        else:
            self.errors = list(errors)
        message = "Invalid ExTetris configuration:\n  - " + "\n  - ".join(self.errors)
        super().__init__(message)


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _is_strict_int(val):
    return isinstance(val, int) and not isinstance(val, bool)


def _is_strict_number(val):
    return isinstance(val, (int, float)) and not isinstance(val, bool)


def _merge_defaults(raw):
    cfg = deepcopy(DEFAULT_CONFIG)
    for key in ("name", "description", "variant", "piece_scope", "connectivity", "max_holes", "renderer"):
        if key in raw:
            cfg[key] = raw[key]
    for section in ("board", "gameplay", "distribution"):
        if section in raw and isinstance(raw[section], dict):
            cfg[section].update(raw[section])
    # Variant-specific sensible defaults when piece_scope/connectivity are omitted
    if "variant" in raw:
        if raw["variant"] == "classic" and "connectivity" not in raw:
            cfg["connectivity"] = "orthogonal"
        if raw["variant"] == "chaos" and "piece_scope" not in raw:
            cfg["piece_scope"] = "fixed"
    return cfg


def validate_config(raw_config):
    """
    Validate a raw configuration dict against schema.json and semantic rules.
    Returns a normalized deep-copied dict with defaults populated, or raises ConfigValidationError.
    """
    if not isinstance(raw_config, dict):
        raise ConfigValidationError(
            f"Root configuration must be a JSON object (dict), got {type(raw_config).__name__}."
        )

    errors = []
    allowed_top = set(DEFAULT_CONFIG.keys())
    unknown_top = sorted(set(raw_config.keys()) - allowed_top)
    if unknown_top:
        errors.append(f"Unknown top-level key(s): {', '.join(unknown_top)}.")

    for section in ("board", "gameplay", "distribution"):
        if section in raw_config and not isinstance(raw_config[section], dict):
            errors.append(f"Section '{section}' must be an object, got {type(raw_config[section]).__name__}.")

    if "board" in raw_config and isinstance(raw_config["board"], dict):
        unknown_b = sorted(set(raw_config["board"].keys()) - set(DEFAULT_CONFIG["board"].keys()))
        if unknown_b:
            errors.append(f"Unknown key(s) in 'board': {', '.join(unknown_b)}.")

    if "gameplay" in raw_config and isinstance(raw_config["gameplay"], dict):
        unknown_g = sorted(set(raw_config["gameplay"].keys()) - set(DEFAULT_CONFIG["gameplay"].keys()))
        if unknown_g:
            errors.append(f"Unknown key(s) in 'gameplay': {', '.join(unknown_g)}.")

    if "distribution" in raw_config and isinstance(raw_config["distribution"], dict):
        unknown_d = sorted(set(raw_config["distribution"].keys()) - set(DEFAULT_CONFIG["distribution"].keys()))
        if unknown_d:
            errors.append(f"Unknown key(s) in 'distribution': {', '.join(unknown_d)}.")

    if errors:
        raise ConfigValidationError(errors)

    cfg = _merge_defaults(raw_config)

    # Top-level field validation
    if not isinstance(cfg["name"], str) or not (1 <= len(cfg["name"].strip()) <= 80):
        errors.append("Field 'name' must be a non-empty string (1..80 chars).")
    if not isinstance(cfg["description"], str) or len(cfg["description"]) > 400:
        errors.append("Field 'description' must be a string of at most 400 characters.")
    if cfg["variant"] not in VALID_VARIANTS:
        errors.append(f"Unknown variant '{cfg['variant']}'. Valid options: {', '.join(VALID_VARIANTS)}.")
    if cfg["piece_scope"] not in VALID_SCOPES:
        errors.append(f"Unknown piece_scope '{cfg['piece_scope']}'. Valid options: {', '.join(VALID_SCOPES)}.")
    if cfg["connectivity"] not in VALID_CONNECTIVITIES:
        errors.append(
            f"Unknown connectivity '{cfg['connectivity']}'. Valid options: {', '.join(VALID_CONNECTIVITIES)}."
        )
    if cfg["max_holes"] is not None:
        if not _is_strict_int(cfg["max_holes"]) or not (0 <= cfg["max_holes"] <= 6):
            errors.append(f"Invalid max_holes={cfg['max_holes']!r}: must be null or an integer in 0..6.")
    if cfg["renderer"] not in VALID_RENDERERS:
        errors.append(f"Unknown renderer '{cfg['renderer']}'. Valid options: {', '.join(VALID_RENDERERS)}.")

    # Board validation
    w = cfg["board"]["width"]
    h = cfg["board"]["height"]
    if not _is_strict_int(w) or not (4 <= w <= 40):
        errors.append(f"Invalid board.width={w!r}: must be an integer between 4 and 40.")
    if not _is_strict_int(h) or not (6 <= h <= 60):
        errors.append(f"Invalid board.height={h!r}: must be an integer between 6 and 60.")

    # Gameplay validation
    spd = cfg["gameplay"]["initial_speed_ms"]
    sf = cfg["gameplay"]["speed_factor"]
    if not _is_strict_int(spd) or not (100 <= spd <= 5000):
        errors.append(f"Invalid gameplay.initial_speed_ms={spd!r}: must be an integer between 100 and 5000 ms.")
    if not _is_strict_number(sf) or not (0.1 < float(sf) <= 1.0):
        errors.append(f"Invalid gameplay.speed_factor={sf!r}: must be a number in (0.1, 1.0].")
    if not isinstance(cfg["gameplay"]["enable_wall_kicks"], bool):
        errors.append("Field 'gameplay.enable_wall_kicks' must be a boolean.")
    if not isinstance(cfg["gameplay"]["enable_ghost"], bool):
        errors.append("Field 'gameplay.enable_ghost' must be a boolean.")

    # Distribution validation
    dist = cfg["distribution"]
    if dist["strategy"] not in VALID_STRATEGIES:
        errors.append(
            f"Unknown distribution.strategy '{dist['strategy']}'. Valid options: {', '.join(VALID_STRATEGIES)}."
        )
    if not _is_strict_int(dist["bag_multiplier"]) or not (1 <= dist["bag_multiplier"] <= 10):
        errors.append(
            f"Invalid distribution.bag_multiplier={dist['bag_multiplier']!r}: must be an integer in 1..10."
        )
    if not _is_strict_number(dist["repeat_penalty"]) or not (0.0 <= float(dist["repeat_penalty"]) <= 1.0):
        errors.append(
            f"Invalid distribution.repeat_penalty={dist['repeat_penalty']!r}: must be a number in [0.0, 1.0]."
        )
    if dist["seed"] is not None and not _is_strict_int(dist["seed"]):
        errors.append(f"Invalid distribution.seed={dist['seed']!r}: must be null or an integer.")
    if not isinstance(dist["weights_by_id"], dict):
        errors.append("Field 'distribution.weights_by_id' must be an object mapping piece IDs to weights.")
    else:
        for pid, weight in dist["weights_by_id"].items():
            if not _is_strict_number(weight) or float(weight) < 0.0:
                errors.append(
                    f"Invalid weight for piece '{pid}' ({weight!r}): weights must be non-negative numbers."
                )
        if dist["strategy"] == "weighted" and dist["weights_by_id"]:
            if sum(float(v) for v in dist["weights_by_id"].values()) <= 0.0:
                errors.append("Weighted distribution requires at least one positive weight in 'weights_by_id'.")

    # Semantic cross-field checks
    if cfg["variant"] == "classic" and cfg["connectivity"] == "diagonal":
        errors.append(
            "Incompatible settings: variant='classic' contains only orthogonal shapes and cannot use connectivity='diagonal'."
        )

    if errors:
        raise ConfigValidationError(errors)

    # Optional jsonschema cross-check if installed
    try:
        import jsonschema
        jsonschema.validate(instance=raw_config, schema=load_schema())
    except ImportError:
        pass
    except Exception as exc:
        raise ConfigValidationError(f"Schema validation error: {exc.message if hasattr(exc, 'message') else exc}")

    return cfg
