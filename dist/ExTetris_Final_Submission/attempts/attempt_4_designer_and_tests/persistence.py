# persistence.py: Game state JSON save/load/resume and text-board export (Attempt 4)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

import json
from pathlib import Path
import numpy

from board import Board
from distributions import (
    AdaptiveDifficultyDistribution,
    BagDistribution,
    MarkovDistribution,
    ShapeDistribution,
    UniformDistribution,
    WeightedDistribution,
)
from factory import ExTetrominoFactory
from hierarchy import classify_extetromino


class PersistenceError(ValueError):
    """Raised when saving or loading ExTetris game state fails."""


def _encode_rng_state(rng):
    state = rng.getstate()
    # Python Random.getstate() -> (version, tuple_of_ints, gauss_next)
    return [state[0], list(state[1]), state[2]]


def _decode_rng_state(encoded):
    return (int(encoded[0]), tuple(int(x) for x in encoded[1]), encoded[2])


def _serialize_piece(piece):
    if piece is None:
        return None
    return {
        "coords": [[int(r), int(c)] for r, c in piece.coords],
        "piece_id": piece.piece_id,
        "name": piece.name,
    }


def _deserialize_piece(data):
    if data is None:
        return None
    coords = [(int(r), int(c)) for r, c in data["coords"]]
    return classify_extetromino(coords, piece_id=data.get("piece_id"), name=data.get("name"))


def _serialize_distribution(dist):
    info = {
        "class": dist.__class__.__name__,
        "seed": getattr(dist, "_seed", None),
        "rng_state": _encode_rng_state(dist.rng) if hasattr(dist, "rng") else None,
        "pool_coords": [
            [[int(r), int(c)] for r, c in s.coords]
            for s in dist.available_shapes()
        ],
        "pool_meta": [
            {"piece_id": s.piece_id, "name": s.name}
            for s in dist.available_shapes()
        ],
    }
    if isinstance(dist, WeightedDistribution):
        info["weights"] = list(dist._weights)
    elif isinstance(dist, BagDistribution):
        info["bag_multiplier"] = dist.bag_multiplier
        info["bag_remaining"] = [_serialize_piece(p) for p in dist._bag]
    elif isinstance(dist, MarkovDistribution):
        info["transition_matrix"] = dist.transition_matrix
        info["last_idx"] = dist._last_idx
    return info


def _deserialize_distribution(info):
    cls_name = info.get("class")
    seed = info.get("seed")
    coords_list = info.get("pool_coords", [])
    meta_list = info.get("pool_meta", [])
    shapes = []
    for idx, raw_coords in enumerate(coords_list):
        meta = meta_list[idx] if idx < len(meta_list) else {}
        shapes.append(
            classify_extetromino(
                [(int(r), int(c)) for r, c in raw_coords],
                piece_id=meta.get("piece_id"),
                name=meta.get("name"),
            )
        )

    if not shapes:
        shapes = ExTetrominoFactory().classic_one_sided()

    if cls_name == "WeightedDistribution":
        dist = WeightedDistribution(shapes, weights=info.get("weights"), seed=seed)
    elif cls_name == "BagDistribution":
        dist = BagDistribution(shapes, bag_multiplier=info.get("bag_multiplier", 1), seed=seed)
        if "bag_remaining" in info and info["bag_remaining"] is not None:
            dist._bag = [_deserialize_piece(p) for p in info["bag_remaining"]]
    elif cls_name == "AdaptiveDifficultyDistribution":
        dist = AdaptiveDifficultyDistribution(shapes, seed=seed)
    elif cls_name == "MarkovDistribution":
        dist = MarkovDistribution(
            shapes,
            transition_matrix=info.get("transition_matrix"),
            seed=seed,
        )
        dist._last_idx = info.get("last_idx")
    else:
        dist = UniformDistribution(shapes, seed=seed)

    if info.get("rng_state") is not None:
        dist.rng.setstate(_decode_rng_state(info["rng_state"]))
    return dist


def save_engine_state(engine, path):
    """Serialize full engine state (board, pieces, cursor, score, FSM, RNG) to JSON."""
    payload = {
        "format": "extetris-state-v1",
        "width": engine.width,
        "height": engine.height,
        "board_grid": [[bool(cell) for cell in row] for row in engine.board.area],
        "state": engine.state.value,
        "score": int(engine.score),
        "lines_cleared": int(engine.lines_cleared),
        "level": int(engine.level),
        "initial_speed_ms": int(engine.initial_speed_ms),
        "speed_factor": float(engine.speed_factor),
        "drop_speed_ms": int(engine.drop_speed_ms),
        "enable_wall_kicks": bool(engine.enable_wall_kicks),
        "enable_ghost": bool(engine.enable_ghost),
        "cursor": [int(engine.cursor[0]), int(engine.cursor[1])],
        "current_piece": _serialize_piece(engine.current_piece),
        "next_piece": _serialize_piece(engine.next_piece),
        "distribution": _serialize_distribution(engine.distribution),
    }
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path


def load_engine_state(path, engine_cls, game_state_enum, custom_distribution=None):
    """Restore an ExTetrisEngine instance from a saved JSON state file."""
    src_path = Path(path)
    if not src_path.exists():
        raise PersistenceError(f"Saved state file not found: {src_path}")
    try:
        data = json.loads(src_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PersistenceError(f"Failed to parse saved state '{src_path}': {exc}") from exc

    if not isinstance(data, dict) or data.get("format") != "extetris-state-v1":
        raise PersistenceError("Invalid or unsupported ExTetris state file format.")

    try:
        width = int(data["width"])
        height = int(data["height"])
        grid = numpy.array(data["board_grid"], dtype=bool)
        if grid.shape != (height, width):
            raise PersistenceError(
                f"Board grid shape {grid.shape} does not match width={width}, height={height}."
            )
        engine = engine_cls(
            width=width,
            height=height,
            distribution=None,
            initial_speed_ms=int(data["initial_speed_ms"]),
            speed_factor=float(data["speed_factor"]),
            enable_wall_kicks=bool(data["enable_wall_kicks"]),
            enable_ghost=bool(data["enable_ghost"]),
        )
        # Assign restored distribution AFTER __init__ so _init_pieces() does not advance its RNG/bag.
        engine.distribution = (
            custom_distribution
            if isinstance(custom_distribution, ShapeDistribution)
            else _deserialize_distribution(data["distribution"])
        )
        engine.board = Board(width=width, height=height)
        engine.board.area = grid
        engine.state = game_state_enum(data["state"])
        engine.score = int(data["score"])
        engine.lines_cleared = int(data["lines_cleared"])
        engine.level = int(data["level"])
        engine.drop_speed_ms = int(data["drop_speed_ms"])
        engine.cursor = (int(data["cursor"][0]), int(data["cursor"][1]))
        engine.current_piece = _deserialize_piece(data["current_piece"])
        engine.next_piece = _deserialize_piece(data["next_piece"])
        return engine
    except PersistenceError:
        raise
    except Exception as exc:
        raise PersistenceError(f"Corrupted state payload: {exc}") from exc


def export_text_board(engine, path):
    """Export human-readable ASCII/Unicode board snapshot (compatible with legacy save_file)."""
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"ExTetris Snapshot | State={engine.state.value} | Score={engine.score} | "
        f"Lines={engine.lines_cleared} | Level={engine.level}\n"
    )
    out_path.write_text(header + str(engine.board), encoding="utf-8")
    return out_path
