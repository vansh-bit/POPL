# ExTetris — Extended Tetris Design and Development

Assignment for **CS F301 Principles of Programming Languages (PoPL), Sem-I, 2026-27**.

## Key Features
- **Zero-Matrix Coordinate Shape Hierarchy (`extetris.shapes`):** Algorithmically generates all **110** unique 4-polyplets on a `4×4` grid (`34` one-sided, `22` free; `7`/`19` classic orthogonal vs. `27`/`91` diagonal) and classifies every piece across **11 bounding boxes** (including `3×4`, `4×3`, and `4×1`), **morphology**, and **landing cavities**.
- **Functional-OO Distributions (`extetris.distributions`):** `UniformDistribution`, `WeightedDistribution`, `BagDistribution`, `AdaptiveDifficultyDistribution`, and `MarkovDistribution` with higher-order combinators (`.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, `>>`).
- **UI-Agnostic FSM Engine (`extetris.engine`):** 4-state FSM (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), Observer callbacks, wall kicks `(0, ±1, ±2)`, ghost projection, level/speed scaling, and bit-identical JSON save/load/resume.
- **Pluggable Renderers (`extetris.renderers`):** `HeadlessRenderer`, cross-platform `CLIRenderer`, and optional `TkinterRenderer`.
- **No-Code Variant Design (`extetris.config`, `extetris.builder`, `ExTetris_Studio.ipynb`):** Schema-validated JSON configs, Fluent `ExTetrisBuilder`, standalone `export_variant()`, and an interactive Jupyter studio.

## Quick Start

```bash
# 1. Install package (editable)
./setup.sh

# 2. Run a preset variant
make run-classic      # 7 classic tetrominoes, 7-Bag, CLI
make run-extended     # 34 one-sided polyplets, Adaptive, CLI
make run-chaos        # 110 fixed orientations, Markov, CLI
make run-gui          # Tkinter GUI window (optional)

# 3. Run full test suite (all 9 categories, incl. clean-venv packaging test)
make test

# 4. Build submission archive (dist/extetris_submission.zip)
make package
```

Or open the no-code interactive designer:
```bash
jupyter notebook ExTetris_Studio.ipynb
```

## Documentation Suite
- [Design Document](docs/DESIGN.md) — Architecture, division of labour, and core design decisions
- [UML Diagrams](docs/UML.md) — Class hierarchy, 4-state FSM, and sequence diagrams (Mermaid)
- [API Reference](docs/API.md) — Application Programmer's Manual for `extetris`
- [Game Programmer's Manual](docs/GAME_PROGRAMMERS_MANUAL.md) — Non-programmer guide for creating and releasing variants
- [Continued Development & AI Usage Report](docs/AI_USAGE_REPORT.md) — Synthesis of Attempts 0–5 and effort analysis
- [Central Verbatim AI Interaction Log](AI_INTERACTION_LOG.md) — Chronological verbatim prompts, responses, fixes, and trade-offs
- [Attempts Archive](attempts/README.md) — Preserved runnable snapshots of Attempts 0–4
