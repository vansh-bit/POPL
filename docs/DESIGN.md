# ExTetris Design Document

## 1. Purpose & Design Philosophy
ExTetris is an extensible Extended Tetris game engine designed for **CS F301 PoPL**. Starting from a monolithic Tkinter prototype (`attempts/attempt_0_appendix_baseline/`) with 73 hard-coded matrices, the final `extetris/` architecture separates concerns into six cohesive layers:

1. **Geometry & Classification (`extetris.shapes`):** Coordinate-first `(r, c)` shapes with zero stored matrices, combinatorial generation of all 110 canonical 4-polyplets on a `4×4` grid, and multi-axis classification by bounding box, topological morphology, and landing cavities.
2. **Board & Heuristics (`extetris.board`):** Bounds-safe grid operations, ghost-row projection, slice-based multi-line clearing, and board-state telemetry (`column_heights`, `get_max_height`, `count_holes`, `get_bumpiness`).
3. **Functional-OO Distributions (`extetris.distributions`):** Seedable strategy objects (`UniformDistribution`, `WeightedDistribution`, `BagDistribution`, `AdaptiveDifficultyDistribution`, `MarkovDistribution`) composable via `.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, and `>>`.
4. **UI-Agnostic FSM Engine & Persistence (`extetris.engine`):** 4-state `GameState` finite state machine (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), Observer callbacks (`register_callback`), wall-kick recovery `(0, ±1, ±2)`, level/speed scaling, and bit-identical JSON save/load/resume.
5. **Pluggable Renderers (`extetris.renderers`):** `AbstractRenderer` implemented by `HeadlessRenderer`, `CLIRenderer` (`termios`/`select` & `msvcrt` non-blocking I/O), and lazy optional `TkinterRenderer`.
6. **Low-Code / No-Code Designer Layer (`extetris.config`, `extetris.builder`, `ExTetris_Studio.ipynb`):** Schema-validated JSON presets, Fluent `ExTetrisBuilder`, standalone variant export (`export_variant()`), and an interactive Jupyter studio sharing a single validation/builder core.

---

## 2. Division of Labour & Entity Relationships

| Subsystem | Package / Module | Core Responsibility | Depends On |
|-----------|------------------|---------------------|------------|
| **Shapes** | `extetris/shapes/{base,hierarchy,factory}.py` | Normalized `(r, c)` geometry, rotations, 110-polyplet synthesis, multi-axis subclasses | `numpy` (only for on-demand `to_matrix()`) |
| **Board** | `extetris/board/board.py` | Grid state, collision detection, ghost projection, line clear, heuristics | `numpy`, `extetris.shapes.Shape` |
| **Distributions** | `extetris/distributions/distributions.py` | Next-piece sampling strategies and functional combinator algebra | `random`, `Shape` interface |
| **Engine** | `extetris/engine/{engine,persistence}.py` | FSM lifecycle, movement, wall kicks, scoring, speed scaling, Observer events, JSON state save/load | `Board`, `ShapeDistribution`, `ExTetrominoFactory` |
| **Renderers** | `extetris/renderers/renderers.py` | Frame formatting, keyboard input polling, display loops | `ExTetrisEngine` public API (optional `tkinter`) |
| **Config & Builder** | `extetris/config/*`, `extetris/builder.py`, `extetris/cli.py` | JSON validation (`schema.json`), fluent assembly, CLI, variant release packaging | All subsystems above |

---

## 3. Key Architectural Decisions

### 3.1 Coordinate Representation Instead of Matrix Initialization (PDF Section 3.2)
- `Shape` stores an immutable sorted tuple of `(r, c)` pairs anchored at `(0, 0)` (`normalize_coords()`).
- Rotations (`rotateCW`, `rotateAntiCW`) and reflections (`fliplr`, `flipud`) transform coordinates directly (`(c, -r)`, `(-c, r)`, `(r, -c)`, `(-r, c)`) and re-anchor at `(0, 0)`.
- `to_matrix()` materializes a boolean `numpy.ndarray` only on demand.
- `ExTetrominoFactory` enumerates all $\binom{16}{4} = 1820$ 4-cell subsets of a `4×4` grid, filters by 8-neighborhood connectivity, and produces:
  - **110** fixed (oriented, normalized) 4-polyplets
  - **34** one-sided 4-polyplets (modulo $90^\circ$ rotations)
  - **22** free 4-polyplets (modulo rotations + reflections)
  - **7** classic one-sided / **19** classic fixed (4-connected `OrthogonalTetromino`) vs. **27** diagonal one-sided / **91** diagonal fixed (`DiagonalPolyplet`)

### 3.2 Multi-Axis Subclass Synthesis & Landing Cavities
Instead of hand-writing $11 \times 2 \times 3 = 66$ boilerplate classes, `extetris.shapes.hierarchy` defines three cooperative-inheritance axes:
1. **Bounding Box (11 classes):** `Box1x4Shape`, `Box4x1Shape`, `Box2x2Shape`, `Box2x3Shape`, `Box3x2Shape`, `Box2x4Shape`, `Box4x2Shape`, `Box3x3Shape`, `Box3x4Shape`, `Box4x3Shape`, `Box4x4Shape`.
2. **Morphology (2 classes):** `OrthogonalTetromino` (4-connected) vs. `DiagonalPolyplet` (corner-connected).
3. **Landing Cavities (3 classes):** `FlatLandingShape` (`0` holes), `SingleCavityShape` (`1` hole), `MultiCavityShape` (`>= 2` holes), where a landing hole is any empty bounding-box cell `(r, c)` lying strictly below an occupied cell `(r', c)` (`r' < r`) in the same column.

`classify_extetromino()` synthesizes and caches composite classes `(box_cls, morph_cls, cavity_cls)` so every piece supports `isinstance()` across all three axes and reclassifies cleanly on `clone()` / `reclassify()` after rotation.

### 3.3 Functional-OO Shape Distributions (PDF Section 3.2)
- Replaces list-index repetition (which also suffered hidden bias in Attempt 0/1 from rotation duplicates) with first-class `ShapeDistribution` objects.
- `AdaptiveDifficultyDistribution` computes normalized board distress:
  $$\text{Distress} = \mathrm{clamp}_{[0,1]}\!\left(0.5 \cdot \frac{H_{\max}}{H_{\text{board}}} + 0.35 \cdot \frac{\text{Holes}}{8} + 0.15 \cdot \frac{\text{Bumpiness}}{15}\right)$$
  and smoothly shifts weight from challenging multi-cavity shapes at low distress to `FlatLandingShape` pieces under high distress.
- Combinators (`FilteredDistribution`, `MappedDistribution`, `BlendedDistribution`, `ConditionalDistribution`) compose via `.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, and `>>` while preserving deterministic seeded RNG behavior.

### 3.4 UI Decoupling, Validation & Persistence
- `ExTetrisEngine` never imports `tkinter` or terminal I/O libraries; `HeadlessRenderer` and `CLIRenderer` work everywhere, and `TkinterRenderer` loads lazily.
- `extetris/config/validator.py` enforces strict types (`not isinstance(val, bool)` for integer fields), rejects unknown keys (`additionalProperties: false`), checks semantic compatibility (e.g., `classic` + `diagonal`), and produces actionable `ConfigValidationError` diagnostics.
- `persistence.py` serializes board grid, pieces, cursor, score, FSM state, and distribution RNG/bag/Markov state, restoring `engine.distribution` **after** `ExTetrisEngine.__init__()` so `BagDistribution` state is never advanced prematurely on resume.
