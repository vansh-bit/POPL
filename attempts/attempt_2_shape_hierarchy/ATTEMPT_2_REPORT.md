# Attempt 2 — Coordinate Shape Hierarchy & 110-Shape Generator Report

- **Status:** Completed (Preserved Snapshot)
- **Directory:** `attempts/attempt_2_shape_hierarchy/`
- **Related Interaction IDs:** `INT-007`, `INT-008`, `INT-009`, `INT-010`, `INT-011` (see [../../AI_INTERACTION_LOG.md](../../AI_INTERACTION_LOG.md))

---

## 1. Objective
Eliminate hard-coded piece matrices (`allextetrominoes.py`) completely in favor of a coordinate-based `Shape` / `ExTetromino` class hierarchy, algorithmically generate all 110 unique canonical 4-polyplets on a `4×4` grid, classify every shape across **bounding box** (including `3×4`, `4×3`, and `4×1`), **morphology**, and **landing-cavity** axes, and run a complete playable and testable game on top of the new hierarchy.

## 2. Files Implemented in `attempts/attempt_2_shape_hierarchy/`
| File | Lines | Role |
|------|-------|------|
| `shape.py` | 221 | Coordinate-only `Shape` (`normalize_coords`, `is_connected`, rotations/flips, on-demand `to_matrix()`, `landing_holes()`, `landing_hole_profile()`) + `ExTetromino` validation |
| `hierarchy.py` | 181 | All 11 bounding-box subclasses (`Box1x4Shape`..`Box4x4Shape`), morphology classes (`OrthogonalTetromino`, `DiagonalPolyplet`), landing-cavity classes (`FlatLandingShape`, `SingleCavityShape`, `MultiCavityShape`), and cached composite classification (`classify_extetromino()`) |
| `factory.py` | 138 | Algorithmic `ExTetrominoFactory` synthesizing 110 fixed / 34 one-sided / 22 free 4-polyplets and separating 7 classic one-sided (19 fixed) from 27 diagonal one-sided (91 fixed) |
| `board.py` | 99 | Coordinate-native, bounds-safe `Board` with `clear_full_lines()` and `clone()` |
| `engine.py` | 266 | Playable & headless-testable `TetrisEngine` wired to `ExTetrominoFactory` and dynamic `reclassify()` on rotation |
| `test_attempt2.py` | 162 | 8-test `unittest` verification suite |

## 3. What Attempt 2 Solved (Verified Results)
1. **Zero Matrix Initialization (`INT-007`, `INT-008`):** Removed `allextetrominoes.py` completely; all pieces are represented by `(r, c)` tuples anchored at `(0, 0)` and synthesized combinatorially in `0.011993` s.
2. **Complete 110-Shape Coverage & Clean Groupings (`INT-008`):**
   - `110` fixed (oriented) 4-polyplets, `34` one-sided, `22` free.
   - `7` classic one-sided (`19` fixed orientations) vs. `27` diagonal one-sided (`91` fixed orientations).
   - Zero duplicate IDs (`1..110`), zero duplicate coordinate sets, 100% 8-connectivity and `(0, 0)` normalization verified.
3. **Full Multi-Axis Subclassing (`INT-009`):**
   - Bounding boxes: `Box1x4Shape` (`1`), `Box4x1Shape` (`1`), `Box2x2Shape` (`1`), `Box2x3Shape` (`12`), `Box3x2Shape` (`12`), `Box2x4Shape` (`14`), `Box4x2Shape` (`14`), `Box3x3Shape` (`33`), `Box3x4Shape` (`10`), `Box4x3Shape` (`10`), `Box4x4Shape` (`2`).
   - Morphology: `OrthogonalTetromino` (`19`), `DiagonalPolyplet` (`91`).
   - Landing cavities (current orientation): `FlatLandingShape` (`8`), `SingleCavityShape` (`21`), `MultiCavityShape` (`81`).
   - Dynamic reclassification on rotation verified (`Box1x4Shape` $\rightarrow$ `Box4x1Shape`).
4. **End-to-End Verification (`INT-010`):**
   - Initial run hit 1 failure in `test_engine_headless_gameplay_and_gameover` due to a test-fixture bug (`board.area[0:2, :] = True` cleared itself via `clear_full_lines()`); fixed obstacle fixture to `board.area[1:4, 3:8] = True`.
   - Final `python3 test_attempt2.py`: **8/8 tests passed in `0.298s`**.

## 4. Remaining Architectural Gaps (Motivating Attempt 3)
1. **No Functional-OO Distribution Framework:** `engine.py` still picks pieces with `self._rng.choice(self.piece_pool)`; there are no `UniformDistribution`, `WeightedDistribution`, `BagDistribution`, `AdaptiveDifficultyDistribution`, or `MarkovDistribution` strategies, nor higher-order combinators (`filter`, `map`, `blend`, `+`, `>>`, `conditional`).
2. **Engine Still Coupled to Tkinter:** `engine.py` (266 lines) still imports `tkinter` at module top level and manages widgets, menus, dialogs, and timers directly rather than using a UI-agnostic 4-state FSM (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`) + Observer callbacks + `AbstractRenderer` (`HeadlessRenderer`, `CLIRenderer`, optional `TkinterRenderer`).
3. **Missing Board Heuristics & Gameplay Polish:** `Board` lacks `count_holes()`, `get_max_height()`, and `get_bumpiness()` metrics needed by adaptive distributions; `TetrisEngine` lacks wall-kick rotation recovery, ghost-piece projection, level progression (`1 + lines_cleared // 10`), and soft/hard drop scoring.
4. **No Designer Configuration / Validation Layer:** Variant setup still requires editing Python code or answering a `stdin` prompt rather than using a Fluent Builder API, validated JSON configuration files, or an interactive notebook studio (addressed in Attempt 4).
