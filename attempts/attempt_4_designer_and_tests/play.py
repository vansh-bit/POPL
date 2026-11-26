# play.py: CLI/GUI Variant Launcher for Attempt 4 (supports --config JSON)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

import argparse
import sys

from builder import ExTetrisBuilder
from config import ConfigValidationError


def main(argv=None):
    parser = argparse.ArgumentParser(description="ExTetris Attempt 4 Variant Launcher")
    parser.add_argument("--config", default="configs/extended.json", help="Path to JSON variant config")
    parser.add_argument("--renderer", choices=["headless", "cli", "tk"], default=None, help="Override configured renderer")
    parser.add_argument("--seed", type=int, default=None, help="Override RNG seed")
    parser.add_argument("--steps", type=int, default=15, help="Ticks for headless renderer")
    args = parser.parse_args(argv)

    try:
        builder = ExTetrisBuilder.from_json(args.config)
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
