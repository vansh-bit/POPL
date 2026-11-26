# Attempt 3 — Decoupled FSM Engine, Functional-OO Distributions & Renderers Report

- **Status:** Completed (Preserved Snapshot)
- **Directory:** `attempts/attempt_3_engine_and_distributions/`
- **Related Interaction IDs:** `INT-012`, `INT-013`, `INT-014`, `INT-015`, `INT-016` (see [../../AI_INTERACTION_LOG.md](../../AI_INTERACTION_LOG.md))

---

## 1. Objective
Decouple the ExTetris core engine completely from Tkinter/UI concerns, replace list-based piece selection with a composable **Functional-OO `ShapeDistribution`** framework, add Board heuristic metrics and modern Tetris gameplay mechanics (4-state FSM, Observer callbacks, wall kicks, ghost projection, level/speed scaling), and prioritize **`HeadlessRenderer`** and **`CLIRenderer`** while making `TkinterRenderer` optional.

## 2. Files Implemented in `attempts/attempt_3_engine_and_distributions/`
| File | Lines | Role |
|------|-------|------|
| `shape.py`, `hierarchy.py`, `factory.py` | 221, 181, 138 | Coordinate-based `Shape` / `ExTetromino` multi-axis hierarchy & 110-polyplet factory |
| `board.py` | 147 | Bounds-safe `Board` + `is_valid_position()`, `get_ghost_row()`, `column_heights()`, `get_max_height()`, `count_holes()`, `get_bumpiness()`, `clone()` |
| `distributions.py` | 326 | `ShapeDistribution` (`Uniform`, `Weighted`, `Bag`, `AdaptiveDifficulty`, `Markov`) + combinators (`.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, `>>`) |
| `engine.py` | 362 | UI-agnostic `ExTetrisEngine` (`GameState`: `READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), Observer `register_callback()`, wall kicks `(0, ±1, ±2)`, ghost composite, level/speed progression |
| `renderers.py` | 389 | `AbstractRenderer`, `HeadlessRenderer`, `CLIRenderer` + `NonBlockingKeyReader` (`termios`/`select` & `msvcrt`), lazy optional `TkinterRenderer` |
| `play.py` | 61 | CLI runner (`--renderer headless|cli|tk`, `--variant`, `--seed`, `--steps`) |
| `test_board_and_distributions.py` | 189 | 7 seeded Board & distribution/combinator tests |
| `test_attempt3.py` | 264 | 8 unified FSM, wall-kick, Observer, renderer & CLI integration tests |

*(Total: 2,278 Python lines; zero `tkinter` imports in `shape.py`, `hierarchy.py`, `factory.py`, `board.py`, `distributions.py`, `engine.py`, or `play.py`.)*

## 3. What Attempt 3 Solved (Verified Results)
1. **Board Heuristic Metrics & Ghost Projection (`INT-012`):** Verified `column_heights`, `get_max_height`, `count_holes`, `get_bumpiness`, and `get_ghost_row` on multi-column stacked boards.
2. **Functional-OO Distributions & Reproducibility (`INT-012`, `INT-015`):**
   - Verified `UniformDistribution`, `WeightedDistribution` (`10:1:1` proportions), `BagDistribution` (exact 7-bag & 2-bag guarantees), `AdaptiveDifficultyDistribution` (distress `0.0` vs `>0.85` flips preference to `FlatLandingShape`), `MarkovDistribution` (`repeat_penalty=0.0` eliminates consecutive duplicates), and exact deterministic seed replay across composed pipelines (`Bag(...).filter(...) >> ...`, `.blend()`, `+`, `.conditional()`).
3. **UI-Agnostic FSM Engine & Gameplay (`INT-013`, `INT-015`):**
   - Verified `READY -> RUNNING -> PAUSED -> RUNNING -> GAME_OVER -> RUNNING`, Observer notifications (`state_changed`, `piece_rotated`, `piece_locked`, `lines_cleared`, `level_up`, `game_over`), `(0, -1)` / `(0, -2)` wall kicks, soft/hard drop (`+1`/`+2`/cell), and `level = 1 + lines_cleared // 10` / `drop_speed_ms = max(100, int(initial_speed * 0.92**(lines // 10)))` with `100ms` floor.
4. **Headless & CLI Priority + Optional Tk (`INT-014`, `INT-015`):**
   - `play.py --renderer headless --variant extended --seed 42 --steps 25` captured 26 frames cleanly.
   - `CLIRenderer` ANSI output, non-TTY safe polling, and keyboard controls passed; `TkinterRenderer` rendered/closed cleanly when Tk was available and raised `RuntimeError` cleanly when Tk was unavailable.
   - **Combined Test Totals:** `test_attempt3.py` (`8/8` in `2.009s`) + `test_board_and_distributions.py` (`7/7` in `1.440s`) = **15/15 tests passing**.

## 4. Remaining Gaps (Motivating Attempt 4)
1. **No Fluent Builder API (`ExTetrisBuilder`):** Programmers still assemble `ExTetrominoFactory`, `ShapeDistribution` chains, `ExTetrisEngine`, and `AbstractRenderer` manually in Python.
2. **No Declarative JSON Configuration & Schema Validation (`extetris/config/`):** There are no `configs/*.json` presets (`classic`, `extended`, `chaos`, `custom`), `schema.json`, or explicit validator providing clear error messages for invalid user configs.
3. **No No-Code Interactive Studio (`ExTetris_Studio.ipynb`):** Non-programmers cannot yet configure, inspect shapes, adjust weights/filters, and launch a custom variant without writing Python code (PDF Section 3).
4. **No Full State Save / Load / Resume Persistence:** Game state serialization (board grid, active/next pieces, cursor, score, lines, level, state, config) is not yet implemented or tested.
5. **No Build/Run Automation or Packaging Verification:** `Makefile`, `setup.sh`, `run.sh`, `test.sh`, and invalid-configuration / persistence / packaging tests remain for Attempts 4 and 5.
