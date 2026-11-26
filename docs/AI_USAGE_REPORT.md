# Continued Development & AI Usage Report (Section 2.2)

- **Project:** Extended Tetris (ExTetris) — CS F301 PoPL, Sem-I, 2026-27
- **Primary AI Assistant Used:** Antigravity (Gemini 4 Hydrogen High / Gemini 3.8 Flash High)
- **Complete Verbatim Log:** [../AI_INTERACTION_LOG.md](../AI_INTERACTION_LOG.md) (`INT-001` through `INT-026`)
- **Preserved Historical Snapshots:** [../attempts/README.md](../attempts/README.md) (`attempt-0-baseline` through `attempt-5-final`)

---

## 1. Development Methodology & Preservation of All Attempts
Rather than jumping straight to a finished codebase or discarding flawed drafts, ExTetris was developed across **six progressive, runnable snapshots (Attempts 0–5)**. Every earlier attempt is preserved in `attempts/` and tagged in Git, and every prompt, response summary, observed failure, manual diagnosis, and architectural trade-off is recorded chronologically in [../AI_INTERACTION_LOG.md](../AI_INTERACTION_LOG.md).

---

## 2. Chronological Progression Across Attempts 0–5

### Attempt 0 — Faithful Appendix A–D Baseline (`attempt-0-baseline`, `INT-001`)
- **Snapshot:** `attempts/attempt_0_appendix_baseline/` (`engine.py`, `board.py`, `shape.py`, `allextetrominoes.py`)
- **What Was Built:** Verbatim transcription of the starter code from `PoPL2026AssignmentExTetris.pdf` without fixing any bugs.
- **Concrete Bugs & Limitations Exposed by Running Probes:**
  1. `allextetrominoes.py` defines **73** matrices containing only **71** unique `(shape, bytes)` entries (`Extetromino1 == Extetromino10 == Extetromino11`, repeating the I-piece as a probability hack) and uses unsafe `eval()`.
  2. `Shape.__init__` aliases `self.matrix = mat` without copying (`Shape.fliplr()` mutated global `Extetromino3` in place).
  3. `Board.collision()` relied on catching `IndexError`, silently returning `False` on negative offsets `(0, -1)` and `(-1, 0)` due to Python/NumPy negative-index wrap-around.
  4. `engine.py` omitted explicit `import numpy` and `tkinter.simpledialog`, relying accidentally on wildcard import leakage; `extetricks_help()` had `self.pasueStatus = False` leaving the game permanently paused; and `TetrisEngine.__init__` blocked inside `window.mainloop()`.

### Attempt 1 — Bug Fixes & Naive Matrix-Backed OOP (`attempt-1-naive-oop`, `INT-002`–`INT-006`)
- **Snapshot:** `attempts/attempt_1_naive_oop/`
- **What Changed:** Added explicit imports, fixed `pauseStatus`/`game_over_status`, added defensive `.copy()` in `Shape.__init__`, fixed `Board.collision()` bounds checks, removed `eval()`, deduplicated `[1, 10, 11]` into `PieceRegistry` (`71` pieces: `7` `ClassicTetromino` + `64` `ExtendedTetromino`), moved `mainloop()` into `run()`, and added `headless=True` (`5/5` gameplay smoke tests passed).
- **Why Attempt 1 Was Still Insufficient (Exposed by Combinatorial Audit, `INT-005`):**
  - Exhaustive enumeration over $\binom{16}{4} = 1820$ subsets of a `4×4` grid proved there are **110** fixed oriented 4-polyplets (**34** one-sided, **22** free). Attempt 1 covered only **71 / 110** fixed orientations (missing **39**) while containing **21 redundant rotation-equivalent groups**, secretly biasing uniform sampling.
  - Pieces were still initialized from hard-coded matrices (violating Section 3.2), lacked bounding-box (`3×4`, `4×3`, etc.) and landing-cavity subclasses, used list sampling, and interleaved Tkinter inside `TetrisEngine`.

### Attempt 2 — Coordinate `Shape` Hierarchy & 110-Shape Generator (`attempt-2-shape-hierarchy`, `INT-007`–`INT-011`)
- **Snapshot:** `attempts/attempt_2_shape_hierarchy/`
- **What Changed:** Eliminated `allextetrominoes.py` completely. Built coordinate-only `Shape` and `ExTetromino`, algorithmic `ExTetrominoFactory` (`110` fixed / `34` one-sided / `22` free; `7`/`19` classic orthogonal vs. `27`/`91` diagonal in `~0.012s`), and cooperative multi-axis classification across all **11 bounding boxes** (including `10` `Box3x4Shape`, `10` `Box4x3Shape`, and `Box4x1Shape`), **morphology** (`OrthogonalTetromino`, `DiagonalPolyplet`), and **landing cavities** (`FlatLandingShape`, `SingleCavityShape`, `MultiCavityShape`).
- **Real Issue Caught & Fixed:** Initial run failed 1 of 8 tests (`test_engine_headless_gameplay_and_gameover` in `0.803s`) because setting `board.area[0:2, :] = True` filled entire rows that `clear_full_lines()` immediately cleared; restricting the obstacle to spawn columns (`area[1:4, 3:8]`) fixed the test (`8/8` passing in `0.298s`).
- **Gaps Remaining:** No Functional-OO distribution combinators, no FSM/Observer engine decoupling, no `Headless`/`CLI` renderers, and no board metrics.

### Attempt 3 — Decoupled FSM Engine, Functional-OO Distributions & Renderers (`attempt-3-engine-and-distributions`, `INT-012`–`INT-016`)
- **Snapshot:** `attempts/attempt_3_engine_and_distributions/`
- **What Changed:** Added `Board` heuristics (`count_holes`, `get_max_height`, `get_bumpiness`, `get_ghost_row`, `clone`), Functional-OO `ShapeDistribution` (`Uniform`, `Weighted`, `Bag`, `AdaptiveDifficulty`, `Markov` + `.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, `>>`), UI-agnostic 4-state FSM `ExTetrisEngine` (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), Observer `register_callback`, wall kicks `(0, ±1, ±2)`, ghost composite, and `AbstractRenderer` (`HeadlessRenderer`, cross-platform `CLIRenderer` using `termios`/`select`/`msvcrt`, lazy optional `TkinterRenderer`).
- **Real Bug Caught & Fixed:** Testing `slow_down()` on `450 ms` revealed IEEE-754 float drift (`450 * 1.1 = 495.00000000000006` caused `math.ceil()` to return `496` instead of `495`). Wrapping speed calculations in `round(..., 6)` resolved it, with **15/15** tests passing (`0.700s` + `0.306s`).

### Attempt 4 — Designer Interface, Validation, Persistence & Categorized Tests (`attempt-4-designer-and-tests`, `INT-017`–`INT-021`)
- **Snapshot:** `attempts/attempt_4_designer_and_tests/`
- **What Changed:** Built strict `config/schema.json`, `config/validator.py` (`ConfigValidationError`), `config/loader.py`, 4 presets (`classic`, `extended`, `chaos`, `custom`), Fluent `ExTetrisBuilder` with `export_variant()`, JSON game-state persistence (`save_state`, `load_state`, `export_text_board`), interactive `ExTetris_Studio.ipynb`, and 8 categorized test modules.
- **Real Bugs Caught & Fixed:**
  1. Initial save/load/resume parity failed on the 4th move after resume because `load_engine_state()` passed the deserialized `BagDistribution` into `ExTetrisEngine.__init__()`, whose `_init_pieces()` popped 2 pieces off `_bag`. Assigning `engine.distribution` post-`__init__` achieved bit-identical resume across all 4 presets + weighted mode.
  2. Initial test run failed 1 of 22 tests (`test_wall_kicks_and_invalid_rotations` in `8.016s`) because blocking row `10` did not block a `4×1` piece rotating into a `1×4` piece on row `8`; moving the wall to row `8` yielded **22/22 passing in `6.638s`**.

### Attempt 5 — Modular Package, Automation, Clean-Venv Verification & Final Docs (`attempt-5-final`, `INT-022`–`INT-026`)
- **Location:** Repository root (`extetris/`, `configs/`, `tests/`, `docs/`, `ExTetris_Studio.ipynb`, `Makefile`, `setup.sh`, `run.sh`, `test.sh`, `pyproject.toml`, `LICENSE`)
- **What Changed:** Promoted Attempt 4 into the installable `extetris` package, added root build/run/test scripts, extracted `extetris/packaging.py` after Make's backslash line-continuation caused an inline `python3 -c` `SyntaxError`, added `tests/test_packaging/test_submission_package.py` to verify `dist/extetris_submission.zip` in an isolated virtual environment, and authored the complete `docs/` suite (`DESIGN.md`, `UML.md`, `API.md`, `GAME_PROGRAMMERS_MANUAL.md`, and this report).

---

## 3. Effort Comparison: With AI Assistance vs. Without AI Assistance

| Activity / Phase | Actual Effort (With AI) | Estimated Effort (Without AI) | Where Human Judgment Was Critical |
|------------------|-------------------------|-------------------------------|-----------------------------------|
| **Starter Baseline Audit & Bug Hunting** (Attempt 0–1) | ~20 min | ~2–3 hours | Identifying subtle Python negative-index wrap-around, namespace leakage, and deciding to preserve Attempt 0 unmodified |
| **Combinatorial 4-Polyplet Math & Multi-Axis Hierarchy** (Attempt 2) | ~25 min | ~4–6 hours | Catching missing `3×4` / `4×3` bounding-box classes, clarifying 7 classic vs. 34 one-sided vs. 110 fixed counts, and defining landing-hole invariants |
| **FSM Engine, Functional-OO Distributions & Renderers** (Attempt 3) | ~35 min | ~6–8 hours | Enforcing UI decoupling, designing seeded combinator reproducibility tests, and catching IEEE-754 `ceil()` drift |
| **JSON Schema, Builder, Persistence, Studio Notebook & Tests** (Attempt 4) | ~45 min | ~6–10 hours | Catching `BagDistribution` premature draw during `load_state()`, testing invalid configs, and enforcing no-code notebook parity |
| **Packaging, Clean-Venv Verification & Documentation** (Attempt 5) | ~40 min | ~4–6 hours | Insisting on isolated venv ZIP verification, verifying every documented CLI/API example, and keeping all historical snapshots intact |
| **Total** | **~2.75 hours** | **~22–33 hours** | **~8–12× speedup**, primarily in boilerplate, test scaffolding, and documentation formatting, while architecture and bug verification remained human-directed |

### Candid Assessment of Trade-Offs
- **Strengths of AI-Assisted Workflow:** Rapid iteration between complete runnable snapshots, fast generation of structured unit tests and Mermaid/Markdown documentation, and immediate cross-checking of combinatorial invariants.
- **Limitations & Risks Observed:** AI-generated test fixtures initially had subtle logic mistakes (e.g., full-row blocker clearing itself in Attempt 2, wrong obstacle row in Attempt 4 wall-kick test, inline Makefile backslash syntax error in Attempt 5, and `BagDistribution` state advance in `load_engine_state`), proving that **every AI output required hands-on execution, inspection, and targeted debugging**.
