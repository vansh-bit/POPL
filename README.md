# ExTetris — Extended Tetris Design and Development

Assignment for **CS F301 Principles of Programming Languages (PoPL), Sem-I, 2026-27**.

## Key Features
- **Zero-Matrix Coordinate Shape Hierarchy (`extetris.shapes`):** Algorithmically generates all **110** unique 4-polyplets on a `4×4` grid (`34` one-sided, `22` free; `7`/`19` classic orthogonal vs. `27`/`91` diagonal) and classifies every piece across **11 bounding boxes** (including `3×4`, `4×3`, and `4×1`), **morphology**, and **landing cavities**.
- **Functional-OO Distributions (`extetris.distributions`):** `UniformDistribution`, `WeightedDistribution`, `BagDistribution`, `AdaptiveDifficultyDistribution`, and `MarkovDistribution` with higher-order combinators (`.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, `>>`).
- **UI-Agnostic FSM Engine (`extetris.engine`):** 4-state FSM (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), Observer callbacks, wall kicks `(0, ±1, ±2)`, ghost projection, level/speed scaling, and JSON save/load/resume (bit-identical state & RNG continuation for all 5 built-in distributions; arbitrary Python-callable combinator compositions restore as a `UniformDistribution` over their materialized shape pool unless a custom `distribution=` is supplied to `load_state()`).
- **Pluggable Renderers (`extetris.renderers`):** `HeadlessRenderer`, cross-platform `CLIRenderer`, and optional `TkinterRenderer`.
- **No-Code Variant Design (`extetris.config`, `extetris.builder`, `ExTetris_Studio.ipynb`):** Schema-validated JSON configs, Fluent `ExTetrisBuilder`, standalone `export_variant()`, and an interactive Jupyter studio.

## Quick Start

### Installation (Normal vs. Offline)
- **Normal installation (recommended, requires network/PyPI index):** Installs `extetris` in editable mode along with its declared dependencies (such as `numpy`):
  ```bash
  ./setup.sh          # or: make setup
  ./setup.sh --venv   # creates and installs into .venv/
  ```
- **Offline installation (uses preinstalled dependencies):** Runs `pip install --no-build-isolation --no-deps -e .` without fetching packages over the network. **Build and runtime dependencies (`setuptools`, `wheel`, `numpy`) must already be installed** in the active Python (or `.venv`) before using `--offline`:
  ```bash
  ./setup.sh --offline
  ```

### Running, Testing & Packaging

```bash
# 1. Run a preset variant
make run-classic      # 7 classic tetrominoes, 7-Bag, CLI
make run-extended     # 34 one-sided polyplets, Adaptive, CLI
make run-chaos        # 110 fixed orientations, Markov, CLI
make run-gui          # Tkinter GUI window (optional)

# 2. Run full test suite (all 9 categories, incl. clean-venv packaging test)
make test

# 3. Build submission archive (dist/extetris_submission.zip)
make package
```

Or open the no-code interactive designer:
```bash
jupyter notebook ExTetris_Studio.ipynb
```

> **Note on Preserved History:** The `attempts/` folder (`attempt_0_appendix_baseline/` through `attempt_4_designer_and_tests/`) and `AI_INTERACTION_LOG.md` preserve every historical development snapshot directly inside the distribution ZIP even though `.git/` metadata is excluded from packaged archives (commit hashes and tags referenced in reports come from the local development Git repository, with no remote URL configured).

## Documentation Suite
- [Design Document](docs/DESIGN.md) — Architecture, division of labour, and core design decisions
- [UML Diagrams](docs/UML.md) — Class hierarchy, 4-state FSM, and sequence diagrams (Mermaid)
- [API Reference](docs/API.md) — Application Programmer's Manual for `extetris`
- [Game Programmer's Manual](docs/GAME_PROGRAMMERS_MANUAL.md) — Non-programmer guide for creating and releasing variants
- [Continued Development & AI Usage Report](docs/AI_USAGE_REPORT.md) — Synthesis of Attempts 0–5 and effort analysis
- [Central Verbatim AI Interaction Log](AI_INTERACTION_LOG.md) — Chronological verbatim prompts, responses, fixes, and trade-offs
- [Attempts Archive](attempts/README.md) — Preserved runnable snapshots of Attempts 0–4
