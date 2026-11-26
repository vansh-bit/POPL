# play.py: CLI entrypoint for ExTetris Attempt 3 (--renderer headless|cli|tk)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

import argparse
import sys

from distributions import (
    AdaptiveDifficultyDistribution,
    BagDistribution,
    MarkovDistribution,
    UniformDistribution,
)
from engine import ExTetrisEngine
from factory import ExTetrominoFactory
from renderers import create_renderer


def build_distribution(variant, factory, seed=None):
    key = variant.strip().lower()
    if key == "classic":
        return BagDistribution(factory.classic_one_sided(), seed=seed)
    if key == "extended":
        return BagDistribution(factory.all_one_sided(), seed=seed)
    if key == "adaptive":
        return AdaptiveDifficultyDistribution(factory.all_fixed(), seed=seed)
    if key == "markov":
        return MarkovDistribution(factory.all_one_sided(), repeat_penalty=0.05, seed=seed)
    raise ValueError(f"Unknown variant '{variant}'. Expected: classic, extended, adaptive, markov.")


def main(argv=None):
    parser = argparse.ArgumentParser(description="ExTetris Attempt 3 Runner")
    parser.add_argument("--renderer", choices=["headless", "cli", "tk"], default="cli")
    parser.add_argument("--variant", choices=["classic", "extended", "adaptive", "markov"], default="extended")
    parser.add_argument("--width", type=int, default=10)
    parser.add_argument("--height", type=int, default=20)
    parser.add_argument("--speed", type=int, default=800)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--steps", type=int, default=15, help="Number of ticks when running headless")
    args = parser.parse_args(argv)

    factory = ExTetrominoFactory()
    dist = build_distribution(args.variant, factory, seed=args.seed)
    engine = ExTetrisEngine(
        width=args.width,
        height=args.height,
        distribution=dist,
        initial_speed_ms=args.speed,
    )
    renderer = create_renderer(args.renderer)
    if args.renderer == "headless":
        frames = renderer.run(engine, steps=args.steps)
        print(frames[-1])
        print(f"Captured {len(frames)} headless frames. Final score={engine.score}, state={engine.state.value}")
    else:
        renderer.run(engine)
    return 0


if __name__ == "__main__":
    sys.exit(main())
