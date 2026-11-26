# cli.py: Package CLI entrypoint (`extetris` / `python -m extetris.cli`)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

import argparse
from pathlib import Path
import sys

from extetris.builder import ExTetrisBuilder
from extetris.config import ConfigValidationError


def _apply_variant_preset(builder, variant):
    key = variant.strip().lower()
    if key == "classic":
        builder.use_classic_tetris().with_distribution("bag")
    elif key == "extended":
        builder.use_extended_tetris().with_distribution("adaptive").with_board_size(12, 22)
    elif key == "chaos":
        builder.use_chaos_tetris().with_distribution("markov").with_board_size(14, 24)
    elif key == "custom":
        builder.use_extended_tetris().filter_diagonal_only().filter_max_holes(2).with_distribution("bag")


def main(argv=None):
    parser = argparse.ArgumentParser(description="ExTetris Game Engine CLI")
    parser.add_argument("--config", default=None, help="Path to a JSON variant configuration file")
    parser.add_argument(
        "--variant",
        choices=["classic", "extended", "chaos", "custom"],
        default="extended",
        help="Built-in variant preset when --config is omitted",
    )
    parser.add_argument("--renderer", choices=["headless", "cli", "tk"], default=None, help="Override renderer")
    parser.add_argument("--seed", type=int, default=None, help="Override RNG seed")
    parser.add_argument("--steps", type=int, default=15, help="Number of ticks for headless renderer")
    parser.add_argument("--export", default=None, help="Export configured variant + docs to directory and exit")
    args = parser.parse_args(argv)

    try:
        if args.config is not None:
            builder = ExTetrisBuilder.from_json(args.config)
        else:
            default_json = Path.cwd() / "configs" / f"{args.variant}.json"
            if default_json.exists():
                builder = ExTetrisBuilder.from_json(default_json)
            else:
                builder = ExTetrisBuilder()
                _apply_variant_preset(builder, args.variant)

        if args.renderer is not None:
            builder.with_renderer(args.renderer)

        if args.seed is not None:
            cfg = builder.get_config()
            builder.with_distribution(
                cfg["distribution"]["strategy"],
                seed=args.seed,
                bag_multiplier=cfg["distribution"]["bag_multiplier"],
                repeat_penalty=cfg["distribution"]["repeat_penalty"],
                weights_by_id=cfg["distribution"].get("weights_by_id"),
            )

        if args.export is not None:
            exported = builder.export_variant(args.export)
            print(
                f"Exported variant ({exported['piece_count']} shapes) to {Path(exported['config']).parent}"
            )
            return 0

        engine, renderer = builder.build()
    except ConfigValidationError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if hasattr(renderer, "frames"):
        frames = renderer.run(engine, steps=args.steps)
        print(frames[-1])
        print(f"Captured {len(frames)} headless frames. Final score={engine.score}, state={engine.state.value}")
    else:
        renderer.run(engine)
    return 0


if __name__ == "__main__":
    sys.exit(main())
