# builder.py: Fluent ExTetrisBuilder API and Variant Exporter (Attempt 4)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from collections import Counter
from copy import deepcopy
from pathlib import Path

from config import ConfigValidationError, get_default_config, load_config, save_config, validate_config
from distributions import (
    AdaptiveDifficultyDistribution,
    BagDistribution,
    MarkovDistribution,
    ShapeDistribution,
    UniformDistribution,
    WeightedDistribution,
)
from engine import ExTetrisEngine
from factory import ExTetrominoFactory
from renderers import create_renderer


class ExTetrisBuilder(object):
    """
    Fluent Builder API enabling game designers and programmers to configure,
    validate, instantiate, and export ExTetris variants cleanly.
    """

    def __init__(self, initial_config=None):
        self._config = validate_config(initial_config) if initial_config is not None else get_default_config()
        self._custom_distribution = None
        self._custom_predicates = []
        self._factory = ExTetrominoFactory()

    @classmethod
    def from_json(cls, path):
        """Construct an ExTetrisBuilder directly from a validated JSON configuration file."""
        cfg = load_config(path)
        return cls(initial_config=cfg)

    def load_json(self, path):
        self._config = load_config(path)
        self._custom_distribution = None
        return self

    def with_name(self, name, description=None):
        self._config["name"] = str(name)
        if description is not None:
            self._config["description"] = str(description)
        return self

    def use_classic_tetris(self):
        self._config["variant"] = "classic"
        self._config["piece_scope"] = "one_sided"
        self._config["connectivity"] = "orthogonal"
        return self

    def use_extended_tetris(self, piece_scope="one_sided"):
        self._config["variant"] = "extended"
        self._config["piece_scope"] = piece_scope
        self._config["connectivity"] = "any"
        return self

    def use_chaos_tetris(self):
        self._config["variant"] = "chaos"
        self._config["piece_scope"] = "fixed"
        self._config["connectivity"] = "any"
        return self

    def filter_max_holes(self, max_holes):
        self._config["max_holes"] = max_holes
        return self

    def filter_orthogonal_only(self):
        self._config["connectivity"] = "orthogonal"
        return self

    def filter_diagonal_only(self):
        self._config["connectivity"] = "diagonal"
        if self._config["variant"] == "classic":
            self._config["variant"] = "custom"
        return self

    def filter_by(self, predicate):
        if not callable(predicate):
            raise TypeError("predicate must be callable.")
        self._custom_predicates.append(predicate)
        return self

    def with_board_size(self, width, height):
        self._config["board"]["width"] = width
        self._config["board"]["height"] = height
        return self

    def with_speed(self, initial_speed_ms, speed_factor=0.92):
        self._config["gameplay"]["initial_speed_ms"] = initial_speed_ms
        self._config["gameplay"]["speed_factor"] = speed_factor
        return self

    def with_wall_kicks(self, enabled=True):
        self._config["gameplay"]["enable_wall_kicks"] = bool(enabled)
        return self

    def with_ghost(self, enabled=True):
        self._config["gameplay"]["enable_ghost"] = bool(enabled)
        return self

    def with_distribution(
        self,
        strategy_or_dist,
        seed=None,
        bag_multiplier=1,
        repeat_penalty=0.1,
        weights_by_id=None,
    ):
        if isinstance(strategy_or_dist, ShapeDistribution):
            self._custom_distribution = strategy_or_dist
        else:
            self._custom_distribution = None
            self._config["distribution"]["strategy"] = str(strategy_or_dist)
            self._config["distribution"]["seed"] = seed
            self._config["distribution"]["bag_multiplier"] = bag_multiplier
            self._config["distribution"]["repeat_penalty"] = repeat_penalty
            if weights_by_id is not None:
                self._config["distribution"]["weights_by_id"] = dict(weights_by_id)
        return self

    def with_renderer(self, renderer_name):
        self._config["renderer"] = str(renderer_name)
        return self

    def get_config(self):
        return deepcopy(self._config)

    def validate(self):
        self._config = validate_config(self._config)
        pool = self.build_piece_pool()
        if not pool:
            raise ConfigValidationError(
                "Current variant and filters leave 0 matching ExTetromino shapes."
            )
        return self._config

    def build_piece_pool(self):
        cfg = validate_config(self._config)
        variant = cfg["variant"]
        scope = cfg["piece_scope"]
        connectivity = cfg["connectivity"]
        max_holes = cfg["max_holes"]

        if variant == "classic":
            pool = self._factory.classic_fixed() if scope == "fixed" else self._factory.classic_one_sided()
        elif variant == "chaos":
            pool = self._factory.all_fixed() if scope == "fixed" else self._factory.all_one_sided()
        else:
            pool = self._factory.all_fixed() if scope == "fixed" else self._factory.all_one_sided()

        if connectivity == "orthogonal":
            pool = [p for p in pool if p.is_orthogonal()]
        elif connectivity == "diagonal":
            pool = [p for p in pool if p.is_diagonal()]

        if max_holes is not None:
            pool = [p for p in pool if p.landing_holes() <= max_holes]

        for pred in self._custom_predicates:
            pool = [p for p in pool if pred(p)]

        return pool

    def build_distribution(self, pool=None):
        if self._custom_distribution is not None:
            return self._custom_distribution

        cfg = validate_config(self._config)
        pieces = pool if pool is not None else self.build_piece_pool()
        if not pieces:
            raise ConfigValidationError("Cannot build distribution from an empty piece pool.")

        dcfg = cfg["distribution"]
        strategy = dcfg["strategy"]
        seed = dcfg["seed"]

        if strategy == "uniform":
            return UniformDistribution(pieces, seed=seed)
        if strategy == "weighted":
            raw_weights = dcfg.get("weights_by_id", {})
            weights = [float(raw_weights.get(str(p.piece_id), raw_weights.get(p.piece_id, 1.0))) for p in pieces]
            if sum(weights) <= 0.0:
                raise ConfigValidationError(
                    "Weighted distribution matched 0 total weight across the selected piece pool."
                )
            return WeightedDistribution(pieces, weights=weights, seed=seed)
        if strategy == "bag":
            return BagDistribution(pieces, bag_multiplier=dcfg["bag_multiplier"], seed=seed)
        if strategy == "adaptive":
            return AdaptiveDifficultyDistribution(pieces, seed=seed)
        if strategy == "markov":
            return MarkovDistribution(pieces, repeat_penalty=dcfg["repeat_penalty"], seed=seed)
        raise ConfigValidationError(f"Unsupported distribution strategy '{strategy}'.")

    def build_engine(self):
        cfg = self.validate()
        pool = self.build_piece_pool()
        dist = self.build_distribution(pool=pool)
        return ExTetrisEngine(
            width=cfg["board"]["width"],
            height=cfg["board"]["height"],
            distribution=dist,
            initial_speed_ms=cfg["gameplay"]["initial_speed_ms"],
            speed_factor=cfg["gameplay"]["speed_factor"],
            enable_wall_kicks=cfg["gameplay"]["enable_wall_kicks"],
            enable_ghost=cfg["gameplay"]["enable_ghost"],
        )

    def build_renderer(self):
        cfg = validate_config(self._config)
        return create_renderer(cfg["renderer"])

    def build(self):
        """Return (ExTetrisEngine, AbstractRenderer) ready to run."""
        engine = self.build_engine()
        renderer = self.build_renderer()
        return engine, renderer

    def export_variant(self, output_dir):
        """
        Release a configured variant into `output_dir` with:
          - variant_config.json
          - VARIANT_README.md (auto-generated designer/player documentation)
          - run_variant.py (launcher script)
        """
        cfg = self.validate()
        pool = self.build_piece_pool()
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        cfg_file = save_config(cfg, out_path / "variant_config.json")

        bbox_counts = Counter(f"{p.height}x{p.width}" for p in pool)
        ortho_n = sum(1 for p in pool if p.is_orthogonal())
        diag_n = len(pool) - ortho_n

        doc_text = "\n".join([
            f"# {cfg['name']}",
            "",
            cfg["description"],
            "",
            "## Variant Rules & Parameters",
            f"- **Variant Mode:** `{cfg['variant']}` (`piece_scope={cfg['piece_scope']}`, `connectivity={cfg['connectivity']}`)",
            f"- **Max Landing Holes Filter:** `{cfg['max_holes']}`",
            f"- **Board Size:** `{cfg['board']['width']} x {cfg['board']['height']}`",
            f"- **Speed Progression:** starts at `{cfg['gameplay']['initial_speed_ms']} ms`, scales by `{cfg['gameplay']['speed_factor']}` every 10 cleared lines (min `100 ms`)",
            f"- **Wall Kicks:** `{cfg['gameplay']['enable_wall_kicks']}` | **Ghost Piece:** `{cfg['gameplay']['enable_ghost']}`",
            f"- **Next-Piece Distribution:** `{cfg['distribution']['strategy']}` (seed=`{cfg['distribution']['seed']}`)",
            f"- **Default Renderer:** `{cfg['renderer']}`",
            "",
            "## Active Piece Pool Summary",
            f"- **Total Shapes Active:** `{len(pool)}` (`{ortho_n}` orthogonal, `{diag_n}` diagonal)",
            f"- **Bounding Box Breakdown:** `{dict(sorted(bbox_counts.items()))}`",
            "",
            "## How to Run",
            "```bash",
            "python3 run_variant.py",
            "```",
            "",
            "## Controls",
            "- Move Left/Right: `a` / `d` or Left/Right Arrow",
            "- Rotate CW / CCW: `w` / Up Arrow (CW), `e` (CCW)",
            "- Soft Drop / Hard Drop: `s` / Down Arrow / Space",
            "- Pause / Quit: `p` / `q`",
            "",
        ])
        doc_file = out_path / "VARIANT_README.md"
        doc_file.write_text(doc_text, encoding="utf-8")

        engine_dir = Path(__file__).resolve().parent
        launcher_code = "\n".join([
            "\"\"\"Auto-generated launcher for exported ExTetris variant.\"\"\"",
            "from pathlib import Path",
            "import sys",
            "",
            "ROOT = Path(__file__).resolve().parent",
            f"ENGINE_DIR = Path({str(engine_dir)!r})",
            "if ENGINE_DIR.exists() and str(ENGINE_DIR) not in sys.path:",
            "    sys.path.insert(0, str(ENGINE_DIR))",
            "",
            "from builder import load_game_from_json",
            "",
            "def main():",
            "    engine, renderer = load_game_from_json(ROOT / 'variant_config.json')",
            "    if hasattr(renderer, 'frames'):",
            "        frames = renderer.run(engine, steps=20)",
            "        print(frames[-1])",
            "    else:",
            "        renderer.run(engine)",
            "",
            "if __name__ == '__main__':",
            "    main()",
            "",
        ])
        launcher_file = out_path / "run_variant.py"
        launcher_file.write_text(launcher_code, encoding="utf-8")

        return {
            "config": cfg_file,
            "docs": doc_file,
            "launcher": launcher_file,
            "piece_count": len(pool),
        }


def load_game_from_json(path):
    """Convenience entrypoint: load, validate, and build (engine, renderer) from JSON."""
    return ExTetrisBuilder.from_json(path).build()
