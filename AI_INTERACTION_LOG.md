# Central AI Interaction Log

> **Assignment Requirement (Section 2.2 & Submission Instructions):**  
> This file is the single chronological source of truth for **verbatim** AI prompts, **verbatim** AI responses, interpretations, plans, implementations, test results, manual modifications/research, and trade-offs across every attempt—including earlier failed or less-successful attempts.  
> Individual `ATTEMPT_N_REPORT.md` files and `docs/AI_USAGE_REPORT.md` reference entries here by Interaction ID (`INT-001`, `INT-002`, ...).

## Metadata
- **Assistant / Tool Used:** Antigravity (Gemini 4 Hydrogen High)
- **Project:** Extended Tetris (ExTetris) — CS F301 PoPL
- **Source Verification:** All 27 entries (`INT-001`–`INT-027`) reproduce exact verbatim prompts and complete, unedited AI responses extracted directly from the session transcript (`transcript_full.jsonl`), separated from implementation artifacts (Section 5) and observed terminal output (Section 6).
- **Git Provenance Note:** Referenced commit hashes and tags come from the local Git repository used during development (no remote URL is configured). Verified release tags: `attempt-0-baseline` (`846e81b`), `attempt-1-naive-oop` (`9e2cfc7`), `attempt-2-shape-hierarchy` (`31ed371`), `attempt-3-engine-and-distributions` (`c091859`), `attempt-4-designer-and-tests` (`c18c89a`), and `attempt-5-final` (`8282631`). *(Earlier intermediate Attempt 5 commits `3d59b1c`, `4e9ee54`, `cfd1a1f`, `fa26c1f`, `fdb216c`, `03a0523` cited inside historical verbatim entries remain valid ancestors on `master`.)* Submission ZIP archives omit `.git/` metadata by design while preserving every runnable attempt snapshot on disk under `attempts/`.

---

## Portability & File Location Guide (External Evaluators)

The verbatim AI responses in Section 2 of `INT-001`–`INT-027` preserve **179** machine-specific file URIs (`file:///Users/vanshsharma/Documents/POPL/...`) exactly as originally output on the development machine. To preserve historical authenticity, those verbatim records have **not** been edited.

To open any file referenced by a verbatim link from the extracted submission archive, strip the prefix `file:///Users/vanshsharma/Documents/POPL/` to obtain its project-relative path (note that historical `#L...` line anchors in `INT-027` reflected line numbers before later log updates). Three items mentioned in historical responses are outside the packaged runtime bundle: `PoPL2026AssignmentExTetris.pdf` (course assignment handout), `answers.txt` (excluded by packaging rules), and pre-built `dist/*.zip` outputs.

### Project-Relative Reference Map (Existing Files in Submission)
- **Root Entrypoints, Configs & Build Scripts:** [README.md](README.md), [ExTetris_Studio.ipynb](ExTetris_Studio.ipynb), [Makefile](Makefile), [pyproject.toml](pyproject.toml), [setup.sh](setup.sh), [run.sh](run.sh), [test.sh](test.sh), [LICENSE](LICENSE), [configs/classic.json](configs/classic.json), [configs/extended.json](configs/extended.json), [configs/chaos.json](configs/chaos.json), [configs/custom.json](configs/custom.json)
- **Final Package (`extetris/`):** [extetris/__init__.py](extetris/__init__.py), [extetris/builder.py](extetris/builder.py), [extetris/cli.py](extetris/cli.py), [extetris/packaging.py](extetris/packaging.py), [extetris/shapes/base.py](extetris/shapes/base.py), [extetris/shapes/hierarchy.py](extetris/shapes/hierarchy.py), [extetris/shapes/factory.py](extetris/shapes/factory.py), [extetris/board/board.py](extetris/board/board.py), [extetris/distributions/distributions.py](extetris/distributions/distributions.py), [extetris/engine/engine.py](extetris/engine/engine.py), [extetris/engine/persistence.py](extetris/engine/persistence.py), [extetris/renderers/renderers.py](extetris/renderers/renderers.py), [extetris/config/schema.json](extetris/config/schema.json), [extetris/config/validator.py](extetris/config/validator.py), [extetris/config/loader.py](extetris/config/loader.py)
- **Documentation (`docs/`):** [docs/DESIGN.md](docs/DESIGN.md), [docs/UML.md](docs/UML.md), [docs/API.md](docs/API.md), [docs/GAME_PROGRAMMERS_MANUAL.md](docs/GAME_PROGRAMMERS_MANUAL.md), [docs/AI_USAGE_REPORT.md](docs/AI_USAGE_REPORT.md)
- **Test Suites (`tests/`):** [tests/test_shapes/test_generation_and_hierarchy.py](tests/test_shapes/test_generation_and_hierarchy.py), [tests/test_board/test_board.py](tests/test_board/test_board.py), [tests/test_rotations/test_rotations_and_wallkicks.py](tests/test_rotations/test_rotations_and_wallkicks.py), [tests/test_distributions/test_distributions.py](tests/test_distributions/test_distributions.py), [tests/test_engine/test_engine_fsm.py](tests/test_engine/test_engine_fsm.py), [tests/test_configuration/test_config_and_builder.py](tests/test_configuration/test_config_and_builder.py), [tests/test_persistence/test_persistence.py](tests/test_persistence/test_persistence.py), [tests/test_integration/test_integration.py](tests/test_integration/test_integration.py), [tests/test_packaging/test_submission_package.py](tests/test_packaging/test_submission_package.py)
- **Preserved Historical Snapshots (`attempts/`):** [attempts/README.md](attempts/README.md), [attempts/attempt_0_appendix_baseline/ATTEMPT_0_REPORT.md](attempts/attempt_0_appendix_baseline/ATTEMPT_0_REPORT.md), [attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md](attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md), [attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md](attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md), [attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md](attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md), [attempts/attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md](attempts/attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md)

---

## Interaction Index

| ID | Attempt | Topic / Goal | Outcome Summary |
|----|---------|--------------|-----------------|
| `INT-001` | Attempt 0 | Reproduce Appendix A–D baseline & run diagnostic probes | Faithful 4-file baseline reproduced; 6 concrete bugs & architectural flaws observed |
| `INT-002` | Attempt 1 | Clone baseline & fix 5 concrete runtime bugs | All 5 bug fixes verified in `attempts/attempt_1_naive_oop/` |
| `INT-003` | Attempt 1 | Naive OOP piece hierarchy & registry refactor | Replaced 73 globals with `PieceRegistry`, `ClassicTetromino`, `ExtendedTetromino` (71 unique) |
| `INT-004` | Attempt 1 | Decouple `mainloop()` / add `headless=True` & run gameplay smoke tests | All 5 headless gameplay smoke tests passed |
| `INT-005` | Attempt 1 | Audit Attempt 1 against PDF Section 3.2 & target design | Quantified 71 vs 110 polyplets, 21 rotation-dup groups, and 4 structural gaps |
| `INT-006` | Attempt 1 | Write `ATTEMPT_1_REPORT.md`, commit & tag `attempt-1-naive-oop` | Report written, logged, committed, and tagged |
| `INT-007` | Attempt 2 | Design coordinate-based `Shape` & `ExTetromino` base classes | Normalized `(r, c)` geometry, rotations, & 4-rotation landing holes verified |
| `INT-008` | Attempt 2 | Build algorithmic `ExTetrominoFactory` (110 4-polyplets) | Generated 110 fixed / 34 one-sided / 22 free / 7 classic (19 fixed) in ~0.012s |
| `INT-009` | Attempt 2 | Implement bounding-box, morphology & landing-cavity subclasses | All 110 shapes verified across 11 boxes (incl. 3×4, 4×3), morphology & cavities |
| `INT-010` | Attempt 2 | Integrate `Board`, `TetrisEngine`, & run `unittest` verification suite | 8/8 unit tests passed (`0.298s`) incl. headless gameplay & Tkinter smoke |
| `INT-011` | Attempt 2 | Audit Attempt 2 gaps, write `ATTEMPT_2_REPORT.md`, commit & tag | Gaps documented; committed & tagged `attempt-2-shape-hierarchy` |
| `INT-012` | Attempt 3 | Implement Board metrics & Functional-OO `ShapeDistribution` | 7/7 seeded board/distribution/combinator tests passed (`0.231s`) |
| `INT-013` | Attempt 3 | Implement UI-agnostic 4-state FSM `ExTetrisEngine` & callbacks | FSM, wall kicks, ghost piece, scoring, level scaling & zero-Tk verified |
| `INT-014` | Attempt 3 | Implement `AbstractRenderer` (`Headless`, `CLI`, optional `Tk`) & `play.py` | Headless sim, ANSI CLI, optional Tk & graceful fallback verified |
| `INT-015` | Attempt 3 | Write & run unified `test_attempt3.py` suite | 8/8 integration tests (`2.009s`) + 7/7 distribution/board tests (`1.440s`) passed |
| `INT-016` | Attempt 3 | Audit Attempt 3 gaps, write `ATTEMPT_3_REPORT.md`, commit & tag | Audited (`2,278` lines); committed & tagged `attempt-3-engine-and-distributions` |
| `INT-017` | Attempt 4 | Implement explicit JSON config schema, validator, loader & presets | 4 presets validated; 14 invalid/malformed config cases cleanly rejected |
| `INT-018` | Attempt 4 | Implement `ExTetrisBuilder`, `export_variant()`, & state persistence | Caught & fixed bag-advance bug on load; bit-identical resume & variant export verified |
| `INT-019` | Attempt 4 | Build & execute `ExTetris_Studio.ipynb` + `play.py` launcher | All 6 code cells executed cleanly via `nbconvert`; `play.py --config` verified |
| `INT-020` | Attempt 4 | Build & run categorized `tests/` suite (all 9 functional areas) | Fixed 1 rotation test fixture; 22/22 tests passed (`6.638s`) |
| `INT-021` | Attempt 4 | Audit Attempt 4, write `ATTEMPT_4_REPORT.md`, commit & tag | Audited (`4,924` lines); committed & tagged `attempt-4-designer-and-tests` |
| `INT-022` | Attempt 5 | Promote `extetris/` package, root `configs/`, & root `ExTetris_Studio.ipynb` | Editable install, `extetris` CLI, `python3 -m extetris.cli`, & notebook verified |
| `INT-023` | Attempt 5 | Add `Makefile`, `setup.sh`, `run.sh`, `test.sh`, root `tests/`, & `make package` | 22/22 root tests (`8.64s`), `extetris/packaging.py`, & 123-file ZIP verified |
| `INT-024` | Attempt 5 | Add clean-venv packaging test (`tests/test_packaging/`) & run full suite | 23/23 tests passed (`38.86s`) incl. isolated venv install, CLI & config check |
| `INT-025` | Attempt 5 | Author `docs/{DESIGN,UML,API,GAME_PROGRAMMERS_MANUAL}.md` & `README.md` | Complete technical, UML, API, and non-programmer docs + verified CLI `--export` |
| `INT-026` | Attempt 5 | Write `docs/AI_USAGE_REPORT.md`, package ZIP, test, commit & tag | Master report written, ZIP rebuilt, full test suite verified & tagged `attempt-5-final` |
| `INT-027` | Attempt 5 | Final Improvement Audit (`PoPL2026AssignmentExTetris.pdf` & Section 6 fixes) | Fixed Tk display probe, `setup.sh` deps, offline packaging skip, & CLI presets |

---

## INT-001 — [Attempt 0] Reproduce Appendix A–D Baseline & Run Diagnostic Probes
- **Timestamp:** 2026-11-26 02:18 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   start attempt 0 only
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   **Attempt 0 (Appendix A–D Baseline)** is complete, preserved, and tagged in Git.

   ### Files Created / Updated
   * Faithfully reproduced starter code (bugs preserved untouched):
     * [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_0_appendix_baseline/engine.py) (253 lines, Appendix A)
     * [board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_0_appendix_baseline/board.py) (97 lines, Appendix B)
     * [shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_0_appendix_baseline/shape.py) (69 lines, Appendix C)
     * [allextetrominoes.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_0_appendix_baseline/allextetrominoes.py) (116 lines, Appendix D)
   * Documentation & Logs:
     * [ATTEMPT_0_REPORT.md](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_0_appendix_baseline/ATTEMPT_0_REPORT.md)
     * [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md) (`INT-001`)
     * [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md) (updated with commit `846e81b` and tag `attempt-0-baseline`)

   ### Key Baseline Findings Observed
   * `python3 shape.py` executed and printed 887 lines.
   * `allextetrominoes.py` defines 73 matrices, of which **71** are unique `(shape, bytes)` pairs (`Extetromino1 == Extetromino10 == Extetromino11`), and `get_extetromino_at(99)` raises `NameError` due to `eval(...)`.
   * `Shape.fliplr()` mutated `allextetrominoes.Extetromino3` in-place because `Shape.__init__` aliases `self.matrix = mat` without copying.
   * `Board.collision()` returned `False` at `(0, -1)` and `(-1, 0)` on an empty `10×20` board due to Python/NumPy negative-index wrap-around.
   * `engine.py` relies on accidental namespace leakage (`numpy` via `from allextetrominoes import *`; `tk.simpledialog` via `from tkinter import filedialog`), has the `self.pasueStatus = False` typo in `extetricks_help()`, and blocks inside `window.mainloop()` during `__init__`.

   Let me know when you're ready to start **Attempt 1 (Naive OOP Refactor)**.
   ````

3. **What I Interpreted:**
   Before changing any design, I needed an exact, unmodified baseline of the starter code from Appendices A–D of `PoPL2026AssignmentExTetris.pdf` so every later improvement and bug fix could be measured against real evidence rather than assumptions.

4. **What I Planned:**
   Transcribe `engine.py`, `board.py`, `shape.py`, and `allextetrominoes.py` verbatim into `attempts/attempt_0_appendix_baseline/`, run targeted non-blocking checks on imports, matrix uniqueness, `Shape` mutation, `Board.collision` boundaries, and `TetrisEngine` runtime traps, and record every flaw in `ATTEMPT_0_REPORT.md`.

5. **What I Implemented:**
   - `attempts/attempt_0_appendix_baseline/engine.py` (253 lines, Appendix A)
   - `attempts/attempt_0_appendix_baseline/board.py` (97 lines, Appendix B)
   - `attempts/attempt_0_appendix_baseline/shape.py` (69 lines, Appendix C)
   - `attempts/attempt_0_appendix_baseline/allextetrominoes.py` (116 lines, Appendix D)

6. **What I Got (Did It Work?):**
   `shape.py`, `board.py`, and `allextetrominoes.py` imported and ran (`python3 shape.py` produced 887 lines of output). However, probing exposed multiple latent bugs and structural issues (including a blocking modal `tk.simpledialog.Dialog` call when triggered without GUI interaction, silent negative-index collision failures, in-place mutation of shared global piece arrays, and accidental `numpy`/`simpledialog` namespace leakage).

   Observed diagnostic output:
   ```text
   --- 1. Import checks ---
   allextetrominoes, shape, board imported OK
   tkinter OK, has simpledialog attr on tk without submodule import?: False
   engine imported OK, has numpy in engine?: True

   --- 2. allextetrominoes audit ---
   Total defined: 73 Exact unique matrices: 68
   Duplicate pair: Extetromino1 == Extetromino10
   Duplicate pair: Extetromino1 == Extetromino11
   Duplicate pair: Extetromino10 == Extetromino11
   Unique (shape, bytes): 71 Duplicate groups: [[1, 10, 11]]
   Same tobytes different shape: [[(1, (1, 4)), (2, (2, 2)), (10, (1, 4)), (11, (1, 4))], [(5, (2, 3)), (22, (3, 2))], [(16, (2, 4)), (64, (4, 2))]]

   --- 3. Shape aliasing & mutation ---
   Extetromino3 mutated in place by Shape.fliplr?: True

   --- 4. Board negative-index wrap-around collision bug ---
   collision at (0, -1) on empty board: False
   collision at (-1, 0) on empty board: False

   --- 5. Tkinter submodule side-effect & eval lookup ---
   simpledialog before filedialog: False
   simpledialog after engine import: True
   get_extetromino_at(99) raised: NameError name 'Extetromino99' is not defined
   python3 shape.py | wc -l -> 887
   ```

7. **How I Got It (Modifications & Independent Research):**
   - Verified PDF OCR against the actual page screenshots (pages 5–16 of `PoPL2026AssignmentExTetris.pdf`) to avoid OCR spacing artifacts (`self . window`) and smart-quote syntax errors (`’`).
   - Verified via Python probes why `engine.py` did not immediately fail with `NameError` on `numpy` (wildcard import `from allextetrominoes import *` leaked `numpy`) and why `tk.simpledialog` was `False` on `import tkinter as tk` until `from tkinter import filedialog` ran.
   - Observed directly during testing (`task-87`) that calling `tk.simpledialog.Dialog(None, ...)` blocks execution waiting for a modal GUI click.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Compact 4-file prototype (535 lines total); immediately playable Tkinter loop; demonstrates the basic tetromino/extetromino concept.
   - **Weaknesses:** Hard-coded 73 matrices (71 distinct shapes; `I` repeated 3× as a probability hack), `eval()`-based piece lookup, negative-index wrap-around collision bug, `Shape` mutating caller matrices in-place, `self.pasueStatus` typo in `extetricks_help`, `TetrisEngine.__init__` blocking inside `window.mainloop()`, and total coupling between UI, I/O, and game logic.

---

## INT-002 — [Attempt 1] Clone Baseline & Fix Five Concrete Bugs
- **Timestamp:** 2026-11-26 10:42 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Copy the Attempt 0 files into attempts/attempt_1_naive_oop/ and fix only the concrete bugs we found in ATTEMPT_0_REPORT.md: (1) add explicit numpy and tkinter.simpledialog imports in engine.py, (2) fix the self.pasueStatus typo and game_over_status handling, (3) make Shape.__init__ copy the input matrix instead of aliasing it and avoid a mutable default argument, (4) fix Board.collision so negative offsets like (0, -1) and (-1, 0) return True instead of wrapping around, and (5) replace eval in allextetrominoes.py and engine.py. Run quick verification checks to prove all five bugs are fixed.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Copied the Attempt 0 files into `attempts/attempt_1_naive_oop/` and fixed all five baseline bugs cleanly:

   ### Fixes Applied
   1. **Explicit imports ([engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py)):** Added `import numpy`, `from tkinter import filedialog, simpledialog`, and replaced `from allextetrominoes import *` with `from allextetrominoes import get_any_extetromino`.
   2. **Typo & game-over state ([engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py)):** Fixed `self.pasueStatus = False` $\rightarrow$ `self.pauseStatus = False` in `extetricks_help()`, set `self.game_over_status = True` on spawn collision, and reset `self.game_over_status = False` in `new_game()`.
   3. **Defensive copy & default argument ([shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/shape.py)):** Changed `mat` default to `None` (creating a fresh default array per instance) and copied `mat.copy()` in `Shape.__init__`.
   4. **Bounds-safe collision ([board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/board.py)):** Updated `Board.collision()` to skip `False` cells and explicitly return `True` when `r < 0`, `r >= self.height`, `c < 0`, or `c >= self.width`.
   5. **Removed `eval()` ([allextetrominoes.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/allextetrominoes.py), [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py), [shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/shape.py)):** Added `EXTETROMINOES` dictionary (`1..73`) with `ValueError` validation in `get_extetromino_at()` and direct `int(input(...))` parsing in `engine.py`.

   ### Verification Output
   `python3 -m py_compile *.py`, `python3 shape.py` (887 lines), and all five AST/runtime assertions passed:
   * `1. Explicit imports & zero eval() calls verified.`
   * `2. pauseStatus typo & game_over_status handling verified.`
   * `3. Shape.__init__ defensive copy & non-mutable default verified.`
   * `4. Board.collision negative offsets & boundaries verified.`
   * `5. Out-of-range lookup safely raised ValueError: Extetromino index out of range: 99 (expected 1..73)`

   Logged verbatim as `INT-002` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 2** whenever you are!
   ````

3. **What I Interpreted:**
   Before redesigning the architecture into OOP classes, we first needed to stabilize the baseline so existing runtime and boundary bugs wouldn't mask later design issues.

4. **What I Planned:**
   Clone `attempt_0_appendix_baseline/*.py` into `attempts/attempt_1_naive_oop/`, apply minimal targeted patches for the 5 bugs, and verify via Python assertions and `py_compile`.

5. **What I Implemented:**
   - [attempts/attempt_1_naive_oop/engine.py](attempts/attempt_1_naive_oop/engine.py): explicit `import numpy` and `from tkinter import filedialog, simpledialog`, explicit `from allextetrominoes import get_any_extetromino`, fixed `self.pauseStatus = False`, set `self.game_over_status = True` on game over and reset in `new_game()`, replaced `eval(...)` in `__main__` with `int(input(...)) + 8` clamped to `8..74`.
   - [attempts/attempt_1_naive_oop/shape.py](attempts/attempt_1_naive_oop/shape.py): replaced mutable default with `mat=None`, copied `mat.copy()` in `Shape.__init__`, and used `get_extetromino_at(i)` in `__main__`.
   - [attempts/attempt_1_naive_oop/board.py](attempts/attempt_1_naive_oop/board.py): updated `Board.collision()` to skip empty cells and explicitly reject negative or out-of-bounds `(r, c)` coordinates.
   - [attempts/attempt_1_naive_oop/allextetrominoes.py](attempts/attempt_1_naive_oop/allextetrominoes.py): added `EXTETROMINOES` dictionary (`1..73`) and replaced `eval(...)` in `get_extetromino_at` and `get_any_extetromino` with safe dictionary lookups raising `ValueError`.

6. **What I Got (Did It Work?):**
   Yes—all 5 verification assertions and `python3 shape.py` (887 lines) passed with exit code `0`.

   Observed verification output:
   ```text
   1. Explicit imports & zero eval() calls verified.
   2. pauseStatus typo & game_over_status handling verified.
   3. Shape.__init__ defensive copy & non-mutable default verified.
   4. Board.collision negative offsets & boundaries verified.
   5. Out-of-range lookup safely raised ValueError: Extetromino index out of range: 99 (expected 1..73)
        887
   ```

7. **How I Got It (Modifications & Independent Research):**
   An initial `inspect.getsource()` substring check for `eval(` flagged a commented-out test snippet inside `board.py` (`# shape=Shape(eval(...))`); switched the verification check to `ast.parse()` / `ast.walk()` to confirm zero executable `eval()` calls across all 4 modules.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Safe bounds checking, no global matrix aliasing, explicit dependencies, zero `eval()`.
   - **Weaknesses:** Still hard-codes 73 matrices (with duplicates `[1, 10, 11]`), still has no piece class hierarchy or Functional-OO distribution, and `TetrisEngine.__init__` still blocks inside `window.mainloop()`.

---

## INT-003 — [Attempt 1] Naive OOP Piece Hierarchy & Registry Refactor
- **Timestamp:** 2026-11-26 10:46 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Now refactor attempts/attempt_1_naive_oop/ into an initial naive OOP design: keep the existing matrix definitions for now, but replace the raw Extetromino1..Extetromino73 globals and eval() lookups with a clean piece registry and simple Shape subclasses (e.g., ClassicTetromino for pieces 1–7 and ExtendedTetromino for the rest), removing the duplicate I-piece entries ([1, 10, 11]). Verify piece lookup, rotation, and uniqueness.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Refactored `attempts/attempt_1_naive_oop/` into an initial OOP registry and class hierarchy:

   ### Changes Made
   1. **`Shape` subclasses ([shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/shape.py)):**
      * Added `ClassicTetromino` (`is_classic = True`) and `ExtendedTetromino` (`is_classic = False`) inheriting from `Shape`.
      * Added `Shape.clone()` (preserving subclass type across rotations) and `Shape.bounding_box()`, plus `.copy()` in `transpose()` so transpose views don't alias memory.
   2. **Piece registry & deduplication ([allextetrominoes.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/allextetrominoes.py)):**
      * Removed all 73 `Extetromino*` globals and replaced them with `PieceRegistry` (`7` classic + `64` extended = **71** unique matrices, removing duplicate I-pieces `#10` and `#11`).
      * Added `create_piece(index)`, `get_any_piece(distribution)`, and `total_pieces()`, keeping `get_extetromino_at()` / `get_any_extetromino()` compatible.
   3. **Engine subclass preservation ([engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py)):**
      * Updated `rotate_CW()` and `rotate_AntiCW()` to use `self.piece.clone()` instead of `Shape(self.piece.matrix)`.
      * Updated `new_piece()` to instantiate via `get_any_piece()` and adjusted the `__main__` index bound to `total_pieces() + 1`.

   ### Verification Output
   * `1. Zero Extetromino* globals verified.`
   * `2. 71 unique matrices verified (duplicates [1, 10, 11] removed).`
   * `3. Exact parity with Attempt 0 deduplicated catalog verified.`
   * `4. Subclasses (7 Classic, 64 Extended), clone(), and 4-rotation invariance verified for all 71 pieces.`
   * `python3 shape.py` exited cleanly (`934` lines printed).

   Logged verbatim as `INT-003` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 3** whenever you are!
   ````

3. **What I Interpreted:**
   Before discarding matrices altogether in Attempt 2, trying a straightforward matrix-backed OOP refactor lets us remove global namespace clutter and test whether simple `ClassicTetromino`/`ExtendedTetromino` subclasses already expose limitations.

4. **What I Planned:**
   Add `ClassicTetromino` and `ExtendedTetromino` + `clone()` in `shape.py`, replace `Extetromino1..73` with `PieceRegistry` in `allextetrominoes.py` (dropping duplicate I-pieces 10 & 11), update `engine.py` to use `get_any_piece()` and `self.piece.clone()`, and verify parity/rotations across all 71 pieces.

5. **What I Implemented:**
   - [attempts/attempt_1_naive_oop/shape.py](attempts/attempt_1_naive_oop/shape.py): added `clone()`, `bounding_box()`, `ClassicTetromino`, and `ExtendedTetromino`.
   - [attempts/attempt_1_naive_oop/allextetrominoes.py](attempts/attempt_1_naive_oop/allextetrominoes.py): removed all 73 `Extetromino*` globals; added `_CLASSIC_SPECS` (7), `_EXTENDED_SPECS` (64), `PieceRegistry`, `create_piece()`, `get_any_piece()`, and `total_pieces()`.
   - [attempts/attempt_1_naive_oop/engine.py](attempts/attempt_1_naive_oop/engine.py): updated `rotate_CW`, `rotate_AntiCW`, `new_piece`, and `__main__` clamp (`min(total_pieces() + 1, ...)`).

6. **What I Got (Did It Work?):**
   Yes—all 71 deduplicated pieces instantiate as `ClassicTetromino` (7) or `ExtendedTetromino` (64), match Attempt 0's unique matrix set exactly, pass `CW + AntiCW` and 4× `CW` rotation invariance without mutating the registry, and `python3 shape.py` prints 934 lines cleanly.

   Observed verification output:
   ```text
   1. Zero Extetromino* globals verified.
   2. 71 unique matrices verified (duplicates [1, 10, 11] removed).
   3. Exact parity with Attempt 0 deduplicated catalog verified.
   4. Subclasses (7 Classic, 64 Extended), clone(), and 4-rotation invariance verified for all 71 pieces.
        934
   ```

7. **How I Got It (Modifications & Independent Research):**
   Noticed that `engine.py`'s `rotate_CW` and `rotate_AntiCW` originally did `Shape(self.piece.matrix)`, which silently stripped `ClassicTetromino`/`ExtendedTetromino` back down to base `Shape`; added `Shape.clone()` so rotation preserves subclass type. Also added `transpose()` `.copy()` in `shape.py` so NumPy transpose views don't alias underlying memory.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Clean registry lookup, zero duplicate pieces, subclass type preserved on rotation, backward-compatible matrix helpers.
   - **Weaknesses:** Still violates Section 3.2's "no matrix initialization" requirement because `_CLASSIC_SPECS`/`_EXTENDED_SPECS` hard-code boolean matrices, misses shapes outside the starter 71, has no bounding-box or landing-cavity subclasses, and still uses list-repetition sampling in `get_any_piece()`.

---

## INT-004 — [Attempt 1] Decouple `mainloop()` / Add Headless Mode & Gameplay Smoke Tests
- **Timestamp:** 2026-11-26 10:48 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   In attempts/attempt_1_naive_oop/engine.py, decouple self.window.mainloop() out of __init__ into a run() method (or add an optional headless=True mode) so we can run automated gameplay tests on movement, CW/CCW rotation, line clearing, and game-over detection without popping up a Tkinter window, while keeping python3 engine.py playable. Run those smoke tests and show the exact output.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Decoupled `window.mainloop()` and timer scheduling out of `TetrisEngine.__init__` into `run()`, and added `headless=False` mode in [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py):

   ### Changes Made
   * Extracted `TetrisEngine.run()` to schedule `update_step()` / `move_down_step()` and start `window.mainloop()` (called by `__main__` so `python3 engine.py` remains playable).
   * Added `headless=False` to `TetrisEngine.__init__`, guarding Tkinter widget/dialog/timer calls when `headless=True`.
   * Added `event=None` defaults and `self.game_over_status` guards to input handlers (`rotate_CW`, `rotate_AntiCW`, `move_left`, `move_right`, `drop_piece`) so they work identically from Tkinter events and programmatic tests.

   ### Exact Smoke Test Output
   `python3 -m py_compile *.py` and the headless gameplay smoke suite exited with code `0`:
   ```text
   SMOKE 1 PASS: Movement & wall boundaries OK, rightmost cursor = (0, 6)
   SMOKE 2 PASS: CW/CCW rotation, subclass preservation & collision rejection OK
   SMOKE 3 PASS: Pause/resume input gating OK
   SMOKE 4 PASS: Line clearing OK, deleted_lines = 1
   SMOKE 5 PASS: Game-over detection & new_game() reset OK
   ```

   Logged verbatim as `INT-004` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 4** whenever you are!
   ````

3. **What I Interpreted:**
   Because `TetrisEngine.__init__` originally started `window.mainloop()`, the engine could not be tested programmatically or run without a GUI window. Separating construction from `run()` and supporting `headless=True` lets us verify core gameplay mechanics cleanly.

4. **What I Planned:**
   Move Tkinter `after()` timers and `mainloop()` into `TetrisEngine.run()`, guard Tk widget references when `headless=True`, keep `if __name__ == "__main__":` calling `tetris_engine.run()`, and write inline smoke assertions covering walls, rotations, pause gating, line clearing, and game over/reset.

5. **What I Implemented:**
   - [attempts/attempt_1_naive_oop/engine.py](attempts/attempt_1_naive_oop/engine.py): added `headless=False` parameter to `TetrisEngine.__init__`, extracted `TetrisEngine.run()`, added `game_over_status` guards in input handlers, added bounds check in `render()`, and updated `__main__` to call `tetris_engine.run()`.

6. **What I Got (Did It Work?):**
   Yes—`py_compile` succeeded and all 5 headless smoke tests (`Movement`, `CW/CCW Rotation`, `Pause/Resume`, `Line Clearing`, `Game Over & Reset`) passed cleanly with exit code `0`.

   Observed output:
   ```text
   SMOKE 1 PASS: Movement & wall boundaries OK, rightmost cursor = (0, 6)
   SMOKE 2 PASS: CW/CCW rotation, subclass preservation & collision rejection OK
   SMOKE 3 PASS: Pause/resume input gating OK
   SMOKE 4 PASS: Line clearing OK, deleted_lines = 1
   SMOKE 5 PASS: Game-over detection & new_game() reset OK
   ```

7. **How I Got It (Modifications & Independent Research):**
   Noticed while writing `render()` and `move_down_step()` guards that `rotate_CW`, `rotate_AntiCW`, `move_left`, `move_right`, and `drop_piece` originally required a Tkinter `event` parameter and only checked `pauseStatus` (not `game_over_status`). Added `event=None` defaults and `self.game_over_status` guards so methods work identically from both Tkinter bindings and headless API calls.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Engine mechanics can now be tested deterministically without a display server while preserving interactive Tkinter play via `run()`.
   - **Weaknesses:** Tkinter widget logic, keyboard callbacks, and game state still live inside one `TetrisEngine` class using `if not self.headless:` branches rather than a true UI-agnostic engine + Renderer abstraction (addressed in Attempt 3).

---

## INT-005 — [Attempt 1] Audit Against PDF Section 3.2 & Target Design
- **Timestamp:** 2026-11-26 10:52 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Audit attempts/attempt_1_naive_oop/ against the requirements in PoPL2026AssignmentExTetris.pdf (Section 3.2) and answers.txt. Specifically check: (1) how many unique 4-polyplets are actually covered vs. missing, (2) why wrapping hard-coded matrices still violates the no-matrix-initialization requirement and lacks bounding-box/morphology/cavity classification, (3) why list-based probability distribution is still crude, and (4) why Tkinter coupling still limits extensibility
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Here is the audit of `attempts/attempt_1_naive_oop/` against [PoPL2026AssignmentExTetris.pdf](file:///Users/vanshsharma/Documents/POPL/PoPL2026AssignmentExTetris.pdf) (Section 3.2) and [answers.txt](file:///Users/vanshsharma/Documents/POPL/answers.txt):

   ---

   ### 1. Exact 4-Polyplet Coverage vs. Missing Shapes
   Running an exhaustive 8-connected search over all $\binom{16}{4} = 1820$ 4-cell subsets on a $4 \times 4$ grid produced:
   * **Total 8-connected 4-polyplets (fitting in $\le 4\times 4$):**
     * **110** fixed (oriented, normalized) shapes
     * **34** one-sided shapes (modulo $90^\circ$ rotations)
     * **22** free shapes (modulo rotations + reflections)
   * **Attempt 1 (`71` matrices in [allextetrominoes.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/allextetrominoes.py)):**
     * Covers **71 / 110** fixed orientations $\rightarrow$ **39 fixed orientations are missing**.
     * Covers **34 / 34** one-sided and **22 / 22** free equivalence classes, **but** contains **21 redundant rotation-duplicate groups** (e.g., `[6, 21]`, `[23, 36, 48, 52]`, `[24, 41, 44, 51]`).
     * **Bounding boxes actually observed in Attempt 1:** `(1,4): 1`, `(2,2): 1`, `(2,3): 7`, `(2,4): 10`, `(3,2): 3`, `(3,3): 33`, `(3,4): 5`, `(4,2): 4`, `(4,3): 5`, `(4,4): 2` — confirming that `(3, 4)` and `(4, 3)` exist in the polyplet family and must be included in Attempt 2's class hierarchy.

   ### 2. Why Hard-Coded Matrix Wrapping Violates Section 3.2
   * Section 3.2 explicitly requires: *"Not initializing any ExTetrominos to matrix or other data values, but instead providing a class heirarchy, classified by shapes, bounding boxes, holes produced while landing in different orientations."*
   * In Attempt 1, `_CLASSIC_SPECS` and `_EXTENDED_SPECS` still hard-code raw boolean matrices, and `Shape` still stores `self.matrix` as its primary representation rather than normalized coordinates.
   * `ClassicTetromino` and `ExtendedTetromino` in [shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/shape.py) are marker subclasses only—they do not override constructors by geometry and lack classification by **bounding box**, **morphology** (`OrthogonalTetromino` vs. `DiagonalPolyplet`), and **landing cavities** (`FlatLandingShape`, `SingleCavityShape`, `MultiCavityShape`).

   ### 3. Why List-Based Probability Distribution Is Still Crude
   * `get_any_piece(distribution=range(1, 72))` still samples uniformly by index from a sequence, requiring index repetition to weight pieces—exactly the *"crude strategy"* Section 3.2 asks to replace with a **functional-OO** design.
   * Worse, because 21 one-sided shapes appear multiple times in different rotations inside `1..71`, even a "uniform" `range(1, 72)` secretly gives 4-orientation entries $4\times$ the probability of 1-orientation entries.
   * There are no composable distribution classes (`Uniform`, `Weighted`, `Bag`, `AdaptiveDifficulty`, `Markov`) or combinators (`filter`, `map`, `blend`, `+`, `>>`, `conditional`).

   ### 4. Why Tkinter Coupling Still Limits Extensibility
   * Even with `headless=True` and `run()`, [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py) still imports `tkinter`, `filedialog`, and `simpledialog` at module top level and scatters `if not self.headless:` branches through game logic (`move_down_step`, `new_game`, `extetricks_help`).
   * It lacks an `AbstractRenderer` (`HeadlessRenderer`, `CLIRenderer`, optional `TkinterRenderer`), an explicit 4-state FSM (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), Observer callbacks, `Board` metrics (`count_holes`, `get_max_height`, `get_bumpiness`, `clone`), and any no-code designer interface (`ExTetrisBuilder`, JSON schema, `ExTetris_Studio.ipynb`).

   Logged verbatim as `INT-005` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 5** to finalize `ATTEMPT_1_REPORT.md` and commit/tag Attempt 1!
   ````

3. **What I Interpreted:**
   This audit establishes the exact mathematical and architectural evidence showing why Attempt 1's matrix-wrapped OOP approach is insufficient and why Attempt 2 and Attempt 3 are necessary.

4. **What I Planned:**
   Compute the exact count of fixed (110), one-sided (34), and free (22) 8-connected 4-polyplets on a `4×4` grid, compare them with Attempt 1's 71 matrices, inspect bounding boxes, and evaluate Section 3.2 / target-architecture gaps.

5. **What I Implemented:**
   Ran a non-destructive Python combinatorial audit script over `attempts/attempt_1_naive_oop/allextetrominoes.py`. (No code edits in this step.)

6. **What I Got (Did It Work?):**
   Yes—the audit revealed that Attempt 1 covers 71 of 110 fixed orientations (missing 39) while containing 21 redundant rotation-equivalent groups across the 34 one-sided polyplets, and confirmed 5 shapes each in `(3, 4)` and `(4, 3)` bounding boxes.

   Observed audit output:
   ```text
   All 8-connected 4-polyplets fitting in <=4x4:
     Fixed (oriented, normalized): 110
     One-sided (modulo 90-deg rotations): 34
     Free (modulo rotations + reflections): 22
   Attempt 1 (71 matrices) coverage:
     Fixed unique: 71
     One-sided unique (rotation equivalence classes): 34
     Free unique: 22
     Missing one-sided 4-polyplets: 0
     Missing fixed 4-polyplets: 39
     Bounding boxes in Attempt 1: [((1, 4), 1), ((2, 2), 1), ((2, 3), 7), ((2, 4), 10), ((3, 2), 3), ((3, 3), 33), ((3, 4), 5), ((4, 2), 4), ((4, 3), 5), ((4, 4), 2)]
     Attempt 1 groups that are rotations of the same one-sided polyplet: 21 groups -> [[6, 21], [8, 9], [10, 16], [11, 18], [13, 19], [15, 17], [20, 22], [23, 36, 48, 52], [24, 41, 44, 51], [25, 31, 37, 55]]
   ```

7. **How I Got It (Modifications & Independent Research):**
   Checked all `C(16, 4) = 1820` 4-cell subsets of a `4×4` grid with BFS 8-neighborhood connectivity and normalized `(0, 0)` coordinates, comparing fixed, 90°-rotation-canonical (one-sided), and dihedral-canonical (free) equivalence classes against Attempt 1's `PIECE_REGISTRY`.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Proves mathematically what the starter catalog actually contains (`71` fixed / `34` one-sided / `22` free) and exposes hidden probability bias from rotation duplicates.
   - **Weaknesses Exposed (motivating Attempts 2–4):** Hard-coded matrices remain, bounding-box/morphology/cavity subclasses do not exist yet, probability distribution is still index-list sampling, and Tkinter remains imported and interleaved inside `TetrisEngine`.

---

## INT-006 — [Attempt 1] Finalize Report, Commit, and Tag
- **Timestamp:** 2026-11-26 10:53 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Write attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md, update AI_INTERACTION_LOG.md with all Attempt 1 interactions verbatim, commit Attempt 1 to Git, tag it attempt-1-naive-oop, and update attempts/README.md with the commit hash.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   **Attempt 1 (Naive OOP Refactor)** is complete, verified, and tagged in Git.

   ### Summary of Deliverables
   * **Report:** [ATTEMPT_1_REPORT.md](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md)
   * **Code Snapshot:** `attempts/attempt_1_naive_oop/` ([engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/engine.py), [board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/board.py), [shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/shape.py), [allextetrominoes.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop/allextetrominoes.py))
   * **Logs & Index:**
     * [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md) updated with all Attempt 1 interactions (`INT-002` through `INT-006`)
     * [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md) updated (`4831027`, tag `attempt-1-naive-oop`, index commit `ab56d94`)

   Let me know when you're ready for **Attempt 2 (Coordinate `Shape` Hierarchy & 110-Shape Generator)**—I can also suggest a step-by-step prompt sequence for Attempt 2 if you'd like!
   ````

3. **What I Interpreted:**
   Attempt 1 is verified and audited, so we lock its snapshot in Git with full documentation before moving to Attempt 2's coordinate-based shape redesign.

4. **What I Planned:**
   Synthesize all Attempt 1 findings (`INT-002`..`INT-005`) into `ATTEMPT_1_REPORT.md`, commit and tag `attempt-1-naive-oop`, and record the commit hash in `attempts/README.md`.

5. **What I Implemented:**
   - [attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md](attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md).

6. **What I Got (Did It Work?):**
   Attempt 1 preserved cleanly in Git with `attempt-1-naive-oop` tag and clean working tree.

7. **How I Got It (Modifications & Independent Research):**
   Confirmed all Attempt 1 interactions (`INT-002` through `INT-006`) reference exact observed verification outputs before committing.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Reproducible, runnable v1 snapshot showing genuine progression from Attempt 0's crashes to a working naive OOP version, along with empirical reasons for Attempt 2.
   - **Weaknesses:** Intentionally leaves coordinate geometry, 110-polyplet synthesis, Functional-OO distributions, and UI decoupling to Attempts 2–3.

---

## INT-007 — [Attempt 2] Coordinate-Based `Shape` & `ExTetromino` Base Classes
- **Timestamp:** 2026-11-26 11:11 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   In attempts/attempt_2_shape_hierarchy/, design the new coordinate-based Shape and ExTetromino base classes without initializing any shape from hard-coded matrices. Store pieces as normalized (r, c) coordinate sets anchored at (0, 0), support rotateCW(), rotateAntiCW(), fliplr(), flipud(), bounding_box(), to_matrix(), and landing_holes() (counting empty cells trapped directly beneath occupied cells in the current orientation and across all 4 rotations). Verify rotations and normalization on sample pieces.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented the coordinate-based `Shape` and `ExTetromino` base classes in [attempts/attempt_2_shape_hierarchy/shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/shape.py) with zero hard-coded matrix storage.

   ### What Was Implemented
   * **`normalize_coords()` & `is_connected()`:** Anchors arbitrary `(r, c)` coordinates at `(0, 0)`, rejects duplicates/empty inputs, and checks 4- or 8-neighborhood connectivity.
   * **`Shape`:** Stores normalized `(r, c)` tuples; implements `rotateCW()`, `rotateAntiCW()`, `fliplr()`, `flipud()`, `bounding_box()`, `to_matrix()` (computed on demand), `landing_holes()`, and `landing_hole_profile()` across all 4 rotations.
   * **`ExTetromino(Shape)`:** Enforces 4 cells and 8-connectivity, and adds `is_orthogonal()`, `is_diagonal()`, `canonical_one_sided()`, and `canonical_free()`.

   ### Verification Output
   `py_compile`, assertion checks, and `python3 shape.py` all passed (`0`):
   ```text
   1. Normalization anchored at (0, 0) verified: ((0, 0), (0, 1), (1, 1), (2, 2))
   2. CW, AntiCW, 4xCW, fliplr, flipud, bounding_box, and to_matrix verified.
   3. Landing holes & 4-rotation profiles verified: {'I': (0, 0, 0, 0), 'O': (0, 0, 0, 0), 'T': (2, 1, 0, 1), 'Diamond': (3, 3, 3, 3)}
   4. Rejected invalid piece as expected: ExTetromino must have exactly 4 cells, got 3.
   4. Rejected invalid piece as expected: ExTetromino cells must be 8-connected, got ((0, 0), (0, 2), (0, 3), (0, 4)).
   ```

   Logged verbatim as `INT-007` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 2** (`ExTetrominoFactory` for all 110 4-polyplets + classic grouping)!
   ````

3. **What I Interpreted:**
   Eliminating stored matrices in favor of normalized `(r, c)` coordinate tuples satisfies PDF Section 3.2 and makes geometric queries (bounding box, rotation, connectivity, and landing cavities) direct and exact.

4. **What I Planned:**
   Create `Shape` (normalized `(r, c)` representation, affine grid rotations/reflections, on-demand `to_matrix()`, and `landing_holes()` / `landing_hole_profile()`) and `ExTetromino(Shape)` (enforcing 4 cells + 8-connectivity and providing 4-connectivity vs. diagonal morphology checks).

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/shape.py](attempts/attempt_2_shape_hierarchy/shape.py): `normalize_coords()`, `is_connected()`, `Shape`, and `ExTetromino`.

6. **What I Got (Did It Work?):**
   Yes—normalization from negative/shifted offsets, rotation/reflection parity against NumPy (`np.rot90`, `np.fliplr`, `np.flipud`), landing-hole profiles across 4 rotations, and validation rejections for invalid cell counts and disconnected pieces all passed with exit code `0`.

   Observed output:
   ```text
   1. Normalization anchored at (0, 0) verified: ((0, 0), (0, 1), (1, 1), (2, 2))
   2. CW, AntiCW, 4xCW, fliplr, flipud, bounding_box, and to_matrix verified.
   3. Landing holes & 4-rotation profiles verified: {'I': (0, 0, 0, 0), 'O': (0, 0, 0, 0), 'T': (2, 1, 0, 1), 'Diamond': (3, 3, 3, 3)}
   4. Rejected invalid piece as expected: ExTetromino must have exactly 4 cells, got 3.
   4. Rejected invalid piece as expected: ExTetromino cells must be 8-connected, got ((0, 0), (0, 2), (0, 3), (0, 4)).
   ```

7. **How I Got It (Modifications & Independent Research):**
   Unified overhangs above a flat floor and internal enclosed voids under a single column-scan invariant: within the bounding box `(h, w)`, an empty `(r, c)` is a landing hole iff an occupied `(r', c)` exists strictly above it (`r' < r`). Verified on `I`, `O`, `T`, `L`, diagonal diamond, and a `3×4` diagonal piece.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Zero hard-coded matrix storage; exact O(1)-cell coordinate transforms; unified landing-hole calculation across all 4 rotations; backward-compatible `matrix` property via `to_matrix()`.
   - **Weaknesses:** Still needs the algorithmic 110-polyplet generator (`ExTetrominoFactory`) and the concrete bounding-box / morphology / landing-cavity subclass hierarchy (Prompts 2–3).

---

## INT-008 — [Attempt 2] Algorithmic `ExTetrominoFactory` (110 4-Polyplets & Classic Grouping)
- **Timestamp:** 2026-11-26 11:17 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Build ExTetrominoFactory in attempts/attempt_2_shape_hierarchy/ to algorithmically generate all 110 unique normalized 8-connected 4-polyplets on a 4×4 grid from scratch (zero hard-coded boolean arrays). Also expose clean queries/groupings distinguishing the 7 classic one-sided tetrominoes (and their 19 fixed orientations) from the 34 one-sided and 110 fixed 4-polyplets. Verify total counts, 8-connectivity, normalization, and zero duplicate IDs
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented the algorithmic `ExTetrominoFactory` in [attempts/attempt_2_shape_hierarchy/factory.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/factory.py) with zero hard-coded boolean matrices.

   ### What Was Implemented
   * **Algorithmic Generation:** Enumerates all $\binom{16}{4}$ 4-cell combinations on a $4\times 4$ grid, filters for 8-connectivity, normalizes to `(0, 0)`, and assigns deterministic IDs `1..110`.
   * **Groupings & Queries:**
     * `all_fixed()` (**110**), `all_one_sided()` (**34**), `all_free()` (**22**)
     * `classic_one_sided()` (**7** edge-connected), `classic_fixed()` (**19** fixed orientations)
     * `extended_one_sided()` (**27** diagonal), `extended_fixed()` (**91** fixed orientations)
     * `by_id()`, `filter(predicate)`, and `summary()`, all returning isolated clones.

   ### Verification Output
   `py_compile`, `python3 factory.py`, and all assertions exited with code `0`:
   ```text
   ExTetrominoFactory summary: {'fixed_total': 110, 'one_sided_total': 34, 'free_total': 22, 'classic_one_sided': 7, 'classic_fixed': 19, 'diagonal_one_sided': 27, 'diagonal_fixed': 91, 'generation_time_sec': 0.011993}
   1. All combinatorial counts verified: 110 fixed, 34 one-sided, 22 free, 7/19 classic, 27/91 diagonal.
   2. Zero duplicate IDs and zero duplicate coordinate sets verified.
   3. 8-connectivity and (0, 0) normalization verified on all 110 shapes.
   4. Clone isolation and by_id() verified.
   ```

   Logged verbatim as `INT-008` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 3** (bounding-box, morphology, and landing-cavity subclasses)!
   ````

3. **What I Interpreted:**
   Rather than storing or fixing the 71 starter matrices from Attempt 1, generating all 4-polyplets combinatorially from `(r, c)` coordinates guarantees completeness (110 fixed, 34 one-sided, 22 free) and lets us separate classic 4-connected tetrominoes (7 one-sided / 19 fixed) cleanly from diagonal polyplets (27 / 91).

4. **What I Planned:**
   Enumerate `C(16, 4)` subsets on a `4×4` grid, filter via `is_connected(..., diagonal=True)`, normalize via `normalize_coords()`, order deterministically into IDs `1..110`, return clones from all query methods, and include an `_instantiate_piece()` hook for Prompt 3's subclass hierarchy.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/factory.py](attempts/attempt_2_shape_hierarchy/factory.py): `ExTetrominoFactory` with `all_fixed`, `all_one_sided`, `all_free`, `classic_one_sided`, `classic_fixed`, `extended_one_sided`, `extended_fixed`, `by_id`, `filter`, and `summary`.

6. **What I Got (Did It Work?):**
   Yes—all 110 fixed, 34 one-sided, 22 free, 7 classic one-sided, 19 classic fixed, 27 diagonal one-sided, and 91 diagonal fixed counts, normalization invariants, 8-connectivity, unique IDs `1..110`, and clone isolation passed in `0.011993` seconds.

   Observed output:
   ```text
   ExTetrominoFactory summary: {'fixed_total': 110, 'one_sided_total': 34, 'free_total': 22, 'classic_one_sided': 7, 'classic_fixed': 19, 'diagonal_one_sided': 27, 'diagonal_fixed': 91, 'generation_time_sec': 0.011993}
   1. All combinatorial counts verified: 110 fixed, 34 one-sided, 22 free, 7/19 classic, 27/91 diagonal.
   2. Zero duplicate IDs and zero duplicate coordinate sets verified.
   3. 8-connectivity and (0, 0) normalization verified on all 110 shapes.
   4. Clone isolation and by_id() verified.
   ```

7. **How I Got It (Modifications & Independent Research):**
   Confirmed mathematically that 4-connected 4-polyominoes on a `4×4` grid yield exactly the 19 fixed orientations of the 7 classic tetrominoes (`I:2, O:1, L:4, J:4, T:4, S:2, Z:2`), allowing classic grouping directly by topological 4-connectivity without any hard-coded classic matrix list.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Zero hard-coded arrays; sub-15 ms generation; clean separation of fixed vs. one-sided vs. free and classic vs. diagonal groupings; clone-safe catalog.
   - **Weaknesses:** Still instantiates plain `ExTetromino` until Prompt 3 hooks in the bounding-box, morphology, and landing-cavity subclasses.

---

## INT-009 — [Attempt 2] Multi-Axis Classification Hierarchy (`BoundingBox`, `Morphology`, `LandingCavity`)
- **Timestamp:** 2026-11-26 11:18 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Extend attempts/attempt_2_shape_hierarchy/ with the full ExTetromino classification hierarchy: (1) bounding-box subclasses covering all valid 4-polyplet dimensions (1x4, 4x1, 2x2, 2x3, 3x2, 2x4, 4x2, 3x3, 3x4, 4x3, 4x4), (2) morphology classes (OrthogonalTetromino for 4-connected vs. DiagonalPolyplet for corner-connected), and (3) landing-cavity classes (FlatLandingShape, SingleCavityShape, MultiCavityShape based on landing hole profile). Have ExTetrominoFactory instantiate the exact matching subclass for every generated piece and verify all 110 shapes classify cleanly
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented the full multi-axis `ExTetromino` classification hierarchy in [attempts/attempt_2_shape_hierarchy/hierarchy.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/hierarchy.py) and wired it into [factory.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/factory.py):

   ### What Was Implemented
   * **Bounding-box subclasses (all 11 valid dimensions):** `Box1x4Shape`, `Box4x1Shape`, `Box2x2Shape`, `Box2x3Shape`, `Box3x2Shape`, `Box2x4Shape`, `Box4x2Shape`, `Box3x3Shape`, `Box3x4Shape`, `Box4x3Shape`, and `Box4x4Shape`.
   * **Morphology subclasses:** `OrthogonalTetromino` (4-connected) and `DiagonalPolyplet` (corner-connected).
   * **Landing-cavity subclasses:** `FlatLandingShape` (`0` holes), `SingleCavityShape` (`1` hole), and `MultiCavityShape` (`>= 2` holes).
   * **Composite synthesis & factory integration:** `classify_extetromino()` builds cached cooperative-MRO composite classes so every piece returned by `ExTetrominoFactory` satisfies `isinstance()` across all 3 axes and automatically reclassifies on `clone()` / `reclassify()` after rotation.

   ### Verification Output
   ```text
   1. All 110 pieces verified across all 3 classification axes:
      Bounding boxes: [('Box1x4Shape', 1), ('Box2x2Shape', 1), ('Box2x3Shape', 12), ('Box2x4Shape', 14), ('Box3x2Shape', 12), ('Box3x3Shape', 33), ('Box3x4Shape', 10), ('Box4x1Shape', 1), ('Box4x2Shape', 14), ('Box4x3Shape', 10), ('Box4x4Shape', 2)]
      Morphology: {'OrthogonalTetromino': 19, 'DiagonalPolyplet': 91}
      Cavities: {'FlatLandingShape': 8, 'MultiCavityShape': 81, 'SingleCavityShape': 21}
   2. Dynamic reclassification on rotation verified: Box1x4Shape -> Box4x1Shape.
   3. Invariant check rejected mismatched subclass: Box3x4Shape requires bounding box (3, 4), got (2, 2)
   ```

   Logged verbatim as `INT-009` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 4** (integrating `Board` & `TetrisEngine` and running Attempt 2 verification tests)!
   ````

3. **What I Interpreted:**
   To avoid an explosion of 66 hand-written classes (`11 boxes × 2 morphologies × 3 cavities`), we can define the 3 clean axis hierarchies with invariant checks and combine them via cooperative MRO + cached composite subclasses, wired into `ExTetrominoFactory`.

4. **What I Planned:**
   Create `Box1x4Shape`..`Box4x4Shape` (explicitly including `Box3x4Shape`, `Box4x3Shape`, `Box4x1Shape`), `OrthogonalTetromino`/`DiagonalPolyplet`, `FlatLandingShape`/`SingleCavityShape`/`MultiCavityShape`, plus `classify_extetromino()`, and hook `ExTetrominoFactory._instantiate_piece()` to use it.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/hierarchy.py](attempts/attempt_2_shape_hierarchy/hierarchy.py): all 11 bounding-box classes, 2 morphology classes, 3 landing-cavity classes, `get_composite_class()`, and `classify_extetromino()`.
   - [attempts/attempt_2_shape_hierarchy/factory.py](attempts/attempt_2_shape_hierarchy/factory.py): hooked `_instantiate_piece()` to `classify_extetromino()`.

6. **What I Got (Did It Work?):**
   Yes—all 110 generated shapes classified cleanly across all 11 bounding boxes (`10` each in `Box3x4Shape` and `Box4x3Shape`), both morphologies (`19` orthogonal, `91` diagonal), and all 3 cavity categories (`8` flat, `21` single, `81` multi), with dynamic reclassification on rotation and invariant rejection on mismatched construction.

   Observed output:
   ```text
   1. All 110 pieces verified across all 3 classification axes:
      Bounding boxes: [('Box1x4Shape', 1), ('Box2x2Shape', 1), ('Box2x3Shape', 12), ('Box2x4Shape', 14), ('Box3x2Shape', 12), ('Box3x3Shape', 33), ('Box3x4Shape', 10), ('Box4x1Shape', 1), ('Box4x2Shape', 14), ('Box4x3Shape', 10), ('Box4x4Shape', 2)]
      Morphology: {'OrthogonalTetromino': 19, 'DiagonalPolyplet': 91}
      Cavities: {'FlatLandingShape': 8, 'MultiCavityShape': 81, 'SingleCavityShape': 21}
   2. Dynamic reclassification on rotation verified: Box1x4Shape -> Box4x1Shape.
   3. Invariant check rejected mismatched subclass: Box3x4Shape requires bounding box (3, 4), got (2, 2)
   ```

7. **How I Got It (Modifications & Independent Research):**
   Noticed that rotating a classified piece in-place (e.g., `Box1x4Shape.rotateCW()`) changes its bounding box to `(4, 1)` and could break `self.__class__(self.coords)` inside `clone()`. Bound `clone` and `reclassify` on composite classes to `classify_extetromino()` so cloned/rotated instances always receive the up-to-date subclass.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Strict runtime invariant checks per axis, zero boilerplate class explosion, full `isinstance()` support on all 3 axes, and automatic reclassification after rotation.
   - **Weaknesses:** Still needs `Board` and `TetrisEngine` integration in Attempt 2 (Prompt 4) to drive live gameplay with the new hierarchy.

---

## INT-010 — [Attempt 2] Integrate `Board` & `TetrisEngine` + Run Verification Suite
- **Timestamp:** 2026-11-26 11:20 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Update Board and TetrisEngine in attempts/attempt_2_shape_hierarchy/ so the full game runs using the new coordinate-based Shape subclasses and ExTetrominoFactory (both headless=True tests and interactive python3 engine.py). Write and run verification tests covering all 110 generated shapes, bounding boxes (including 3x4 and 4x3), rotations, Board collision boundaries, line clearing, and game-over flow.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Integrated the coordinate-based `Shape` hierarchy and `ExTetrominoFactory` into `Board`, `TetrisEngine`, and a full `unittest` suite in `attempts/attempt_2_shape_hierarchy/`:

   ### Files Created / Updated
   * [board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/board.py) — Coordinate-native `Board` (`_extract_coords`, bounds-safe `insertShape`/`removeShape`/`collision`, `clear_full_lines()`, `clone()`).
   * [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/engine.py) — Updated `TetrisEngine` drawing pieces from `ExTetrominoFactory`, reclassifying rotated pieces via `reclassify()`, rendering directly from `piece.coords`, and supporting both `headless=True` and interactive `python3 engine.py` modes (`1=Classic 7`, `2=One-Sided 34`, `3=All Fixed 110`).
   * [test_attempt2.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/test_attempt2.py) — 8-test `unittest` suite covering all 110 shapes, all 11 bounding boxes (including `3×4` and `4×3`), rotations, `Board` bounds/line clearing, headless gameplay/game-over, and Tkinter GUI initialization.

   ### Verification Output
   *(Note: The first test run failed 1 of 8 tests because `board.area[0:2, :] = True` filled entire rows that `clear_full_lines()` immediately cleared; restricting the obstacle to spawn columns `board.area[1:4, 3:8] = True` fixed the fixture.)*

   Final run (`py_compile` + `python3 test_attempt2.py`):
   ```text
   test_board_boundaries_and_collisions ... ok
   test_engine_headless_gameplay_and_gameover ... ok
   test_multiline_clear_non_adjacent ... ok
   test_tkinter_gui_smoke ... ok
   test_110_unique_connected_normalized_shapes ... ok
   test_bounding_box_morphology_and_cavity_classification ... ok
   test_invalid_subclass_and_extetromino_rejected ... ok
   test_rotations_and_reclassification ... ok

   Ran 8 tests in 0.298s

   OK
   ```

   Logged verbatim as `INT-010` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 5** to write `ATTEMPT_2_REPORT.md`, commit, and tag `attempt-2-shape-hierarchy`!
   ````

3. **What I Interpreted:**
   To prove the new coordinate-based hierarchy works end-to-end (not just in isolation), `Board` and `TetrisEngine` had to operate directly on `Shape.coords` and `ExTetrominoFactory` while supporting both headless automated tests and interactive Tkinter play.

4. **What I Planned:**
   Update `board.py` (`_extract_coords`, `clear_full_lines`, `clone`), rewrite `engine.py` to use `ExTetrominoFactory` and `reclassify()` on rotations, and create `test_attempt2.py` with 8 comprehensive `unittest` cases.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/board.py](attempts/attempt_2_shape_hierarchy/board.py)
   - [attempts/attempt_2_shape_hierarchy/engine.py](attempts/attempt_2_shape_hierarchy/engine.py)
   - [attempts/attempt_2_shape_hierarchy/test_attempt2.py](attempts/attempt_2_shape_hierarchy/test_attempt2.py)

6. **What I Got (Did It Work?):**
   Yes—after fixing the game-over test fixture, all 8 `unittest` tests passed (`Ran 8 tests in 0.298s — OK`), including Tkinter window initialization/cleanup.

7. **How I Got It (Modifications & Independent Research):**
   Diagnosed the initial `AssertionError` in `test_engine_headless_gameplay_and_gameover`: pre-filling entire rows `0:2` caused `move_down_step()` -> `clear_full_lines()` to evaporate the blocker rows before checking spawn collision. Restricting the obstacle to `area[1:4, 3:8]` simulated an authentic stacked tower blocking `(0, 4)` without triggering full-line erasure.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Completely matrix-free `Shape`/`ExTetrominoFactory`/`Board` pipeline; 110 shapes + all 11 bounding boxes verified; `engine.py` maintains exact piece subclass across rotations.
   - **Weaknesses (motivating Attempt 3):** `TetrisEngine` still uses `self._rng.choice(self.piece_pool)` instead of Functional-OO distributions, still embeds Tkinter directly, lacks FSM/Observer architecture, lacks board metrics (`count_holes`, `get_max_height`, `get_bumpiness`), wall kicks, ghost piece, and CLI/Headless renderers.

---

## INT-011 — [Attempt 2] Audit Remaining Gaps, Write Report, Commit & Tag
- **Timestamp:** 2026-11-26 11:22 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Audit attempts/attempt_2_shape_hierarchy/ to highlight what Attempt 2 solved and what architectural gaps remain for Attempt 3 (such as lack of Functional-OO distribution combinators, FSM/Observer engine decoupling, Headless/CLI renderers, wall kicks, and board heuristics). Then write attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md, update AI_INTERACTION_LOG.md, commit Attempt 2, tag it attempt-2-shape-hierarchy, and update attempts/README.md
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   **Attempt 2 (Coordinate Shape Hierarchy & 110-Shape Generator)** is complete, verified, and tagged in Git.

   ### Summary of Deliverables
   * **Report:** [ATTEMPT_2_REPORT.md](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md)
   * **Code Snapshot (`attempts/attempt_2_shape_hierarchy/`):**
     * [shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/shape.py), [hierarchy.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/hierarchy.py), [factory.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/factory.py) (110% Tkinter-free, zero hard-coded matrices)
     * [board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/board.py), [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/engine.py), [test_attempt2.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy/test_attempt2.py) (`8/8` tests passing in `0.298s`)
   * **Logs & Index:**
     * [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md) updated (`INT-007` through `INT-011`)
     * [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md) updated (`31ed371`, tag `attempt-2-shape-hierarchy`, index commit `993dbf3`)

   Ready whenever you want to move on to **Attempt 3** (I can also give you a 5-prompt sequence for Attempt 3 if you'd like)!
   ````

3. **What I Interpreted:**
   With the shape hierarchy and 110-polyplet factory verified, we need an explicit audit of what Attempt 2 resolved vs. what engine, distribution, renderer, and heuristic gaps motivate Attempt 3 before freezing the Attempt 2 snapshot.

4. **What I Planned:**
   Audit Attempt 2 modules for coupling and missing features, capture the synthesis in `ATTEMPT_2_REPORT.md`, commit and tag `attempt-2-shape-hierarchy`, and update `attempts/README.md`.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md](attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md).

6. **What I Got (Did It Work?):**
   Yes—all 6 files audited cleanly, `ATTEMPT_2_REPORT.md` finalized, and the Attempt 2 snapshot is committed and tagged `attempt-2-shape-hierarchy`.

   Observed audit output:
   ```text
   board.py: lines=99, imports_tkinter=False, has_eval=False
   engine.py: lines=266, imports_tkinter=True, has_eval=False
   factory.py: lines=138, imports_tkinter=False, has_eval=False
   hierarchy.py: lines=181, imports_tkinter=False, has_eval=False
   shape.py: lines=221, imports_tkinter=False, has_eval=False
   test_attempt2.py: lines=162, imports_tkinter=True, has_eval=False
   ```

7. **How I Got It (Modifications & Independent Research):**
   Verified module boundaries programmatically (`imports_tkinter` and `has_eval` checks) showing that `shape.py`, `hierarchy.py`, `factory.py`, and `board.py` are now 100% Tkinter-free, leaving UI coupling confined to `engine.py`.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Completely solves PDF Section 3.2's shape-hierarchy and no-matrix requirements with 8/8 passing tests.
   - **Weaknesses:** Engine/distribution/renderer decoupling and non-programmer configuration remain for Attempts 3 and 4.

---

## INT-012 — [Attempt 3] Board Metrics & Functional-OO `ShapeDistribution` Framework
- **Timestamp:** 2026-11-26 11:28 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Create attempts/attempt_3_engine_and_distributions/ building on Attempt 2's coordinate shape hierarchy. First upgrade Board with heuristic metrics (count_holes(), get_max_height(), get_bumpiness(), is_valid_position(), get_ghost_row(), and clone()). Then design the Functional-OO ShapeDistribution hierarchy (UniformDistribution, WeightedDistribution, BagDistribution, AdaptiveDifficultyDistribution, MarkovDistribution) supporting deterministic seeds and higher-order combinators (.filter(), .map(), .blend(), .conditional(), +, and >>). Write seeded tests verifying distribution composition, statistical weights, bag guarantees, adaptive distress response, and exact seed reproducibility.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Bootstrapped `attempts/attempt_3_engine_and_distributions/` with Attempt 2's shape hierarchy and implemented the upgraded `Board` heuristics and Functional-OO `ShapeDistribution` framework:

   ### Files Created
   * [board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/board.py) — Added `is_valid_position()`, `get_ghost_row()`, `column_heights()`, `get_max_height()`, `count_holes()`, `get_bumpiness()`, and `clone()`.
   * [distributions.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/distributions.py) — Implemented `ShapeDistribution` (`UniformDistribution`, `WeightedDistribution`, `BagDistribution`, `AdaptiveDifficultyDistribution`, `MarkovDistribution`) with deterministic seeds and combinators (`.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, `>>`).
   * [test_board_and_distributions.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/test_board_and_distributions.py) — Seeded verification suite.

   ### Exact Test Output
   ```text
   test_heights_holes_bumpiness_and_ghost ... ok
   test_adaptive_difficulty_distress_response ... ok
   test_bag_distribution_guarantees ... ok
   test_combinators_filter_map_blend_add_rshift_conditional ... ok
   test_markov_transitions_and_anti_repeat ... ok
   test_uniform_and_seed_reproducibility ... ok
   test_weighted_statistical_proportions ... ok

   Ran 7 tests in 0.231s

   OK
   ```

   Logged verbatim as `INT-012` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 2** (UI-agnostic 4-state FSM `ExTetrisEngine` & Observer callbacks)!
   ````

3. **What I Interpreted:**
   To replace Attempt 0/1's crude list-repetition sampling with a true Functional-OO design (Section 3.2), distributions must be first-class seeded objects that compose cleanly via `.filter()`, `.map()`, `.blend()`, `.conditional()`, `+`, and `>>`, while `Board` exposes the height/hole/bumpiness telemetry needed by adaptive sampling and ghost projection.

4. **What I Planned:**
   Upgrade `Board` with `is_valid_position`, `get_ghost_row`, `column_heights`, `get_max_height`, `count_holes`, and `get_bumpiness`; build `ShapeDistribution` (`Uniform`, `Weighted`, `Bag`, `AdaptiveDifficulty`, `Markov`) and combinator wrappers (`Filtered`, `Mapped`, `Blended`, `Conditional`); and test both statistical behavior and exact seed reproducibility.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/board.py](attempts/attempt_3_engine_and_distributions/board.py)
   - [attempts/attempt_3_engine_and_distributions/distributions.py](attempts/attempt_3_engine_and_distributions/distributions.py)
   - [attempts/attempt_3_engine_and_distributions/test_board_and_distributions.py](attempts/attempt_3_engine_and_distributions/test_board_and_distributions.py)

6. **What I Got (Did It Work?):**
   Yes—all 7 seeded test suites passed in `0.231s` (`py_compile` + `unittest`), confirming exact board heuristics, ghost landing rows, statistical weight proportions (`10:1:1`), 7-bag / 2-bag guarantees, adaptive distress inversion, Markov transition matrices, and reproducible composed pipelines.

   Observed output:
   ```text
   test_heights_holes_bumpiness_and_ghost ... ok
   test_adaptive_difficulty_distress_response ... ok
   test_bag_distribution_guarantees ... ok
   test_combinators_filter_map_blend_add_rshift_conditional ... ok
   test_markov_transitions_and_anti_repeat ... ok
   test_uniform_and_seed_reproducibility ... ok
   test_weighted_statistical_proportions ... ok

   Ran 7 tests in 0.231s

   OK
   ```

7. **How I Got It (Modifications & Independent Research):**
   Checked seed inheritance across combinators (`blend`, `+`, `filter`, `map`, `conditional`) so composed expressions like `d1.blend(d2, weight=0.8, seed=777)` produce bit-identical sequences across independent runs when given matching component/combinator seeds.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Clean Functional-OO combinator algebra, deterministic seeded testing, zero hard-coded piece data, and board-state-aware adaptive sampling.
   - **Weaknesses:** Still needs the decoupled FSM `ExTetrisEngine` (Prompt 2) and `AbstractRenderer` (`Headless`/`CLI`/optional `Tkinter`) (Prompt 3) to drive full games.

---

## INT-013 — [Attempt 3] UI-Agnostic FSM `ExTetrisEngine` & Observer Callbacks
- **Timestamp:** 2026-11-26 11:29 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Implement the UI-agnostic ExTetrisEngine in attempts/attempt_3_engine_and_distributions/ with an explicit 4-state FSM (READY, RUNNING, PAUSED, GAME_OVER), Observer callbacks (register_callback / event notifications for state, piece lock, line clear, level up, and game over), wall-kick rotation recovery (offsets 0, ±1, ±2), ghost-piece projection, soft/hard drop scoring (+1 / +2 per cell), and level/speed progression (level = 1 + lines_cleared // 10, drop_speed_ms = max(100, int(initial_speed * 0.92**(lines // 10)))). Verify FSM transitions, wall kicks, ghost landing, callbacks, and level scaling without any UI dependency.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented the UI-agnostic `ExTetrisEngine` and `GameState` FSM in [attempts/attempt_3_engine_and_distributions/engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/engine.py) with zero UI/Tkinter imports.

   ### What Was Implemented
   * **4-State FSM (`GameState`):** `READY`, `RUNNING`, `PAUSED`, and `GAME_OVER` with guarded transitions (`start()`, `pause()`, `resume()`, `toggle_pause()`, `new_game()`).
   * **Observer Callbacks:** `register_callback()` supporting both event-specific listeners (`state_changed`, `piece_spawned`, `piece_moved`, `piece_rotated`, `piece_locked`, `lines_cleared`, `level_up`, `speed_changed`, `game_over`, `render_needed`) and wildcard (`"*"`) listeners.
   * **Gameplay Mechanics:** Wall-kick rotation recovery `(0, 0), (0, -1), (0, 1), (0, -2), (0, 2)`, ghost-piece projection (`get_ghost_cursor()`, `get_render_composite()`), soft drop (`+1`), hard drop (`+2`/cell), and level/speed scaling (`level = 1 + lines_cleared // 10`, `drop_speed_ms = max(100, int(initial_speed * 0.92**(lines // 10)))`).

   ### Verification Output
   ```text
   1. Zero tkinter/UI dependency in engine.py verified.
   2. 4-state FSM READY -> RUNNING -> PAUSED -> RUNNING verified.
   3. Wall-kick (0, -2) rotation recovery verified at right wall.
   4. Ghost projection, composite matrix, soft drop (+1) & hard drop (+2/cell) verified.
   5. Level/speed progression (12 lines -> level 2, 920ms) & Observer events verified.
   6. GAME_OVER transition & Observer event verified.
   ```

   Logged verbatim as `INT-013` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 3** (`AbstractRenderer`, `HeadlessRenderer`, `CLIRenderer`, optional `TkinterRenderer`, and `play.py`)!
   ````

3. **What I Interpreted:**
   To completely decouple game rules from presentation, `ExTetrisEngine` must own the 4-state FSM, piece spawning, wall kicks, ghost projection, scoring, and speed progression without importing any UI toolkit, communicating outward strictly through `register_callback()` events and `get_render_composite()`.

4. **What I Planned:**
   Define `GameState` enum (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), implement `ExTetrisEngine` lifecycle methods (`start`, `pause`, `resume`, `toggle_pause`, `new_game`), wall-kick offsets `((0, 0), (0, -1), (0, 1), (0, -2), (0, 2))`, soft/hard drop scoring (`+1`/`+2`), level/speed progression, `get_render_composite()`, and Observer dispatch (`*` + named events).

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/engine.py](attempts/attempt_3_engine_and_distributions/engine.py): `GameState` and `ExTetrisEngine`.

6. **What I Got (Did It Work?):**
   Yes—`py_compile` and all 6 verification assertions passed with exit code `0`, confirming zero `tkinter` imports, exact FSM transitions, `(0, -2)` wall-kick recovery, `+1`/`+2` drop scoring, level `2` (`920 ms`) after 12 lines cleared, and `GAME_OVER` Observer events.

   Observed output:
   ```text
   1. Zero tkinter/UI dependency in engine.py verified.
   2. 4-state FSM READY -> RUNNING -> PAUSED -> RUNNING verified.
   3. Wall-kick (0, -2) rotation recovery verified at right wall.
   4. Ghost projection, composite matrix, soft drop (+1) & hard drop (+2/cell) verified.
   5. Level/speed progression (12 lines -> level 2, 920ms) & Observer events verified.
   6. GAME_OVER transition & Observer event verified.
   ```

7. **How I Got It (Modifications & Independent Research):**
   Supported both `register_callback(event, fn)` and `register_callback(fn)` (wildcard `"*"` listener) so renderers or telemetry hooks can subscribe globally or per-event cleanly. Also ensured `get_render_composite()` prioritizes `active (3)` over `ghost (2)` and `locked (1)` so overlapping spawn/landing cells render accurately.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Completely UI-independent core engine; deterministic tick/step API; Observer notifications; built-in wall-kicks and ghost projection.
   - **Weaknesses:** Still needs `AbstractRenderer` implementations (`HeadlessRenderer`, `CLIRenderer`, optional `TkinterRenderer`) and a runnable `play.py` entrypoint (Prompt 3).

---

## INT-014 — [Attempt 3] `AbstractRenderer` (`Headless`, `CLI`, Optional `Tkinter`) & `play.py`
- **Timestamp:** 2026-11-26 11:30 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Implement AbstractRenderer in attempts/attempt_3_engine_and_distributions/ with priority on HeadlessRenderer (frame capture/inspection for automated runs) and CLIRenderer (ANSI terminal rendering + cross-platform non-blocking input via termios/select on POSIX and msvcrt on Windows), plus an optional TkinterRenderer that degrades gracefully if Tk is unavailable. Add a runnable entrypoint (play.py) supporting --renderer headless|cli|tk and verify HeadlessRenderer and CLIRenderer rendering/frame output (plus optional Tk check).
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented `AbstractRenderer` (`HeadlessRenderer`, `CLIRenderer`, optional `TkinterRenderer`) and `play.py` in `attempts/attempt_3_engine_and_distributions/`:

   ### Files Created
   * [renderers.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/renderers.py) — `AbstractRenderer`, `HeadlessRenderer` (frame/composite/snapshot capture + scripted runner), `CLIRenderer` + `NonBlockingKeyReader` (ANSI output + `termios`/`select` on POSIX & `msvcrt` on Windows), lazy optional `TkinterRenderer` with `is_available()`, and `create_renderer()`.
   * [play.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/play.py) — CLI runner supporting `--renderer headless|cli|tk`, `--variant classic|extended|adaptive|markov`, `--seed`, `--steps`, `--width`, `--height`, and `--speed`.

   ### Verification Output
   `play.py --renderer headless --variant extended --seed 42 --steps 25` and renderer checks passed (`0`):
   ```text
   Captured 26 headless frames. Final score=0, state=RUNNING
   1. HeadlessRenderer scripted simulation verified, frames captured: 6
   2. CLIRenderer ANSI output, key controls, and non-TTY run verified.
   3a. TkinterRenderer.is_available(): True
   3b. Optional TkinterRenderer render & close verified.
   3c. Graceful degradation verified when Tk absent: Tkinter is not available in this Python environment.
   ```

   Logged verbatim as `INT-014` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 4** (`test_attempt3.py` unified integration & reproducibility suite)!
   ````

3. **What I Interpreted:**
   To prove the engine is truly decoupled from UI toolkits, all rendering and input must live behind `AbstractRenderer`, with `HeadlessRenderer` and `CLIRenderer` as first-class targets and `TkinterRenderer` imported lazily so headless/no-display environments never crash.

4. **What I Planned:**
   Create `AbstractRenderer` with `attach/render/run/close`, `HeadlessRenderer` with frame/composite/snapshot capture and scripted actions, `CLIRenderer` with `termios`/`select` + `msvcrt` non-blocking key polling and ANSI frame formatting, lazy `TkinterRenderer` with `is_available()`, and `play.py` CLI runner.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/renderers.py](attempts/attempt_3_engine_and_distributions/renderers.py)
   - [attempts/attempt_3_engine_and_distributions/play.py](attempts/attempt_3_engine_and_distributions/play.py)

6. **What I Got (Did It Work?):**
   Yes—`play.py --renderer headless` captured 26 frames showing active, ghost, and locked extended pieces; `CLIRenderer` rendered ANSI frames and processed key controls in non-TTY streams; and `TkinterRenderer` both ran when Tk was available and raised a clean `RuntimeError` when Tk was mocked absent.

   Observed verification output (`play.py --renderer headless --variant extended --seed 42 --steps 25` + renderer checks):
   ```text
   Captured 26 headless frames. Final score=0, state=RUNNING
   1. HeadlessRenderer scripted simulation verified, frames captured: 6
   2. CLIRenderer ANSI output, key controls, and non-TTY run verified.
   3a. TkinterRenderer.is_available(): True
   3b. Optional TkinterRenderer render & close verified.
   3c. Graceful degradation verified when Tk absent: Tkinter is not available in this Python environment.
   ```

7. **How I Got It (Modifications & Independent Research):**
   Guarded `termios`/`tty` `setcbreak()` behind `input_stream.isatty()` and wrapped `tk.Tk()` / `import tkinter` inside `TkinterRenderer` rather than module top level, ensuring automated test runners and piped streams work without `termios.error` or `ImportError`.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Clean pluggable renderer architecture; zero Tk dependency in core/CLI/headless flows; cross-platform non-blocking keyboard handling.
   - **Weaknesses:** Needs a unified `test_attempt3.py` suite covering all engine/distribution/renderer edge cases together (Prompt 4) and lacks the designer-facing Builder/JSON/Notebook layer (Attempt 4).

---

## INT-015 — [Attempt 3] Unified `test_attempt3.py` Integration & Reproducibility Suite
- **Timestamp:** 2026-11-26 11:32 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Write a comprehensive unittest suite (test_attempt3.py) in attempts/attempt_3_engine_and_distributions/ covering Board metrics, wall kicks, FSM transitions (READY -> RUNNING -> PAUSED -> RUNNING -> GAME_OVER), Observer event logs, seeded distribution reproducibility & combinators (filter, map, blend, +, >>, conditional), HeadlessRenderer, and CLIRenderer output. Run the full suite, fix any bugs or edge cases uncovered, and show exact test results.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Created and ran the unified integration suite [test_attempt3.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/test_attempt3.py) covering Board metrics, wall kicks, 4-state FSM transitions, Observer callbacks, seeded distribution combinators, `HeadlessRenderer`, `CLIRenderer`, `play.py`, and optional `TkinterRenderer` fallback.

   ### Exact Test Output
   All 15 tests across both suites passed after `py_compile`:
   ```text
   test_bounds_metrics_ghost_and_multiline_clear ... ok
   test_seeded_reproducibility_and_bag_filtered ... ok
   test_weighted_bag_markov_adaptive_and_combinators ... ok
   test_fsm_lifecycle_and_observers ... ok
   test_scoring_and_level_speed_floor ... ok
   test_wall_kicks_left_right_and_disabled ... ok
   test_headless_and_cli_renderers_and_play_cli ... ok
   test_optional_tk_graceful_degradation ... ok

   Ran 8 tests in 2.009s

   OK
   ```
   *(Plus all 7 tests in [test_board_and_distributions.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/test_board_and_distributions.py) passed in `1.440s`.)*

   Logged verbatim as `INT-015` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 5** (audit Attempt 3 gaps for Attempt 4, write `ATTEMPT_3_REPORT.md`, commit, and tag `attempt-3-engine-and-distributions`)!
   ````

3. **What I Interpreted:**
   Attempt 3 needs an end-to-end test suite exercising the interactions between `Board`, `ShapeDistribution` combinators, `ExTetrisEngine`, `HeadlessRenderer`, `CLIRenderer`, `TkinterRenderer` fallback, and `play.main()` together.

4. **What I Planned:**
   Write `test_attempt3.py` covering all 4 subsystem areas (board heuristics/bounds, seeded distributions & composed combinators, FSM/wall-kicks/scoring/level-floor/observers, and renderers + CLI), then run both test modules together.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/test_attempt3.py](attempts/attempt_3_engine_and_distributions/test_attempt3.py)

6. **What I Got (Did It Work?):**
   Yes—all 8 tests in `test_attempt3.py` (`2.009s`) and all 7 tests in `test_board_and_distributions.py` (`1.440s`) passed with exit code `0`.

   Observed output:
   ```text
   test_bounds_metrics_ghost_and_multiline_clear ... ok
   test_seeded_reproducibility_and_bag_filtered (__main__.TestDistributionsAndCombinators.test_seeded_reproducibility_and_bag_filtered) ... ok
   test_weighted_bag_markov_adaptive_and_combinators ... ok
   test_fsm_lifecycle_and_observers ... ok
   test_scoring_and_level_speed_floor ... ok
   test_wall_kicks_left_right_and_disabled ... ok
   test_headless_and_cli_renderers_and_play_cli ... ok
   test_optional_tk_graceful_degradation ... ok

   Ran 8 tests in 2.009s

   OK
   ...
   Ran 7 tests in 1.440s

   OK
   ```

7. **How I Got It (Modifications & Independent Research):**
   Tested both obstacle-induced left wall kicks (`(0, -1)` when col 4 was blocked) and right-wall boundary kicks (`(0, -2)`), as well as composed `BagDistribution(...).filter(... ) >> ...` reproducibility and `100ms` minimum drop speed clamping at high line counts.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Full cross-module verification across 15 test cases with deterministic seeds and real CLI/renderer integration checks.
   - **Weaknesses:** Still lacks Attempt 4's designer-facing Builder, JSON schema validation, save/load/resume persistence, and no-code Jupyter studio.

---

## INT-016 — [Attempt 3] Audit Remaining Gaps, Write Report, Commit & Tag
- **Timestamp:** 2026-11-26 11:33 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Audit attempts/attempt_3_engine_and_distributions/ to summarize what Attempt 3 achieved and what designer-facing gaps remain for Attempt 4 (Fluent ExTetrisBuilder, JSON schema loader/validator, save/load/resume persistence, no-code ExTetris_Studio.ipynb, and invalid-configuration tests). Write attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md, update AI_INTERACTION_LOG.md, commit Attempt 3, tag it attempt-3-engine-and-distributions, and update attempts/README.md.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   **Attempt 3 (Decoupled FSM Engine, Functional-OO Distributions & Renderers)** is complete, verified, and tagged in Git.

   ### Summary of Deliverables
   * **Report:** [ATTEMPT_3_REPORT.md](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md)
   * **Code Snapshot (`attempts/attempt_3_engine_and_distributions/`):**
     * [shape.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/shape.py), [hierarchy.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/hierarchy.py), [factory.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/factory.py)
     * [board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/board.py), [distributions.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/distributions.py), [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/engine.py), [renderers.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/renderers.py), [play.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/play.py)
     * Tests: [test_attempt3.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/test_attempt3.py) (`8/8` in `2.009s`) and [test_board_and_distributions.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions/test_board_and_distributions.py) (`7/7` in `1.440s`) — **15/15 passing**
   * **Logs & Index:**
     * [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md) updated (`INT-012` through `INT-016`)
     * [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md) updated (`11e3753`, tag `attempt-3-engine-and-distributions`, index commit `a3e0dba`)

   Ready whenever you want to start **Attempt 4 (Designer Interface, JSON Validation, Persistence, Studio Notebook & Test Suite)**—I can give you the Attempt 4 prompt sequence next if you'd like!
   ````

3. **What I Interpreted:**
   With the decoupled engine, Functional-OO distributions, and multi-renderer layer verified (`15/15` tests), we need to document the boundary audit and remaining no-code designer gaps before freezing Attempt 3.

4. **What I Planned:**
   Inspect module coupling/line counts, write `ATTEMPT_3_REPORT.md` detailing achievements (`INT-012`..`INT-015`) and Attempt 4 gaps, commit and tag `attempt-3-engine-and-distributions`, and update `attempts/README.md`.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md](attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md).

6. **What I Got (Did It Work?):**
   Yes—audit confirmed clean UI isolation (`tkinter` confined to `renderers.py` and its test), `ATTEMPT_3_REPORT.md` finalized, and Attempt 3 tagged in Git.

   Observed audit output:
   ```text
   board.py: lines=147, mentions_tkinter=False
   distributions.py: lines=326, mentions_tkinter=False
   engine.py: lines=362, mentions_tkinter=False
   factory.py: lines=138, mentions_tkinter=False
   hierarchy.py: lines=181, mentions_tkinter=False
   play.py: lines=61, mentions_tkinter=False
   renderers.py: lines=389, mentions_tkinter=True
   shape.py: lines=221, mentions_tkinter=False
   test_attempt3.py: lines=264, mentions_tkinter=True
   test_board_and_distributions.py: lines=189, mentions_tkinter=False
   Total Python lines: 2278
   ```

7. **How I Got It (Modifications & Independent Research):**
   Checked `mentions_tkinter` across all 10 files in `attempt_3_engine_and_distributions/` to verify zero UI leakage back into core modules (`shape`, `hierarchy`, `factory`, `board`, `distributions`, `engine`, `play`).

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Complete, tested engine/distribution/renderer core ready for the no-code designer interface in Attempt 4.
   - **Weaknesses:** Still requires Python code to configure variants until Attempt 4 adds `ExTetrisBuilder`, JSON schema validation, persistence, and `ExTetris_Studio.ipynb`.

---

## INT-017 — [Attempt 4] Explicit JSON Configuration Schema, Validator & Presets
- **Timestamp:** 2026-11-26 11:36 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Create attempts/attempt_4_designer_and_tests/ building on Attempt 3. First implement explicit configuration handling (config/schema.json, config/validator.py, config/loader.py) with ConfigValidationError producing clear, human-readable error messages for invalid board sizes, unknown variants/distributions/renderers, invalid hole/speed/seed values, or malformed JSON. Also create four declarative presets (configs/classic.json, configs/extended.json, configs/chaos.json, configs/custom.json) and verify both valid loading and invalid-configuration rejection.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented explicit JSON configuration handling and the four declarative presets in `attempts/attempt_4_designer_and_tests/`:

   ### Files Created
   * Configuration module: [schema.json](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/config/schema.json), [validator.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/config/validator.py) (`ConfigValidationError`, `validate_config`), [loader.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/config/loader.py) (`load_config`, `save_config`, `get_default_config`)
   * Presets (`attempts/attempt_4_designer_and_tests/configs/`): [classic.json](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/configs/classic.json), [extended.json](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/configs/extended.json), [chaos.json](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/configs/chaos.json), [custom.json](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/configs/custom.json)

   ### Verification Output
   * All 4 presets loaded and validated cleanly.
   * All 14 invalid/incompatible/malformed configuration cases (`small_board`, `unknown_variant`, `unknown_dist`, `unknown_renderer`, `negative_holes`, `bool_holes`, `too_fast_speed`, `bad_seed_type`, `bool_seed`, `unknown_key_typo`, `classic_plus_diagonal`, `negative_weight`, `malformed_json`, `missing_file`) raised `ConfigValidationError` with exact field/line diagnostics.

   Logged verbatim as `INT-017` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 2** (Fluent `ExTetrisBuilder`, variant export, and save/load/resume persistence)!
   ````

3. **What I Interpreted:**
   Non-programmer configuration relies on catching typos, out-of-range parameters, and semantic mismatches upfront with actionable error messages rather than failing deep inside engine or numpy code.

4. **What I Planned:**
   Define a strict `schema.json` (`additionalProperties: false`), implement `validate_config()` with strict integer vs. boolean guards (`not isinstance(val, bool)`) and semantic checks (e.g., `classic` + `diagonal`), wrap JSON parse/IO errors cleanly in `load_config()`, and author the 4 presets (`classic`, `extended`, `chaos`, `custom`).

5. **What I Implemented:**
   - [attempts/attempt_4_designer_and_tests/config/schema.json](attempts/attempt_4_designer_and_tests/config/schema.json)
   - [attempts/attempt_4_designer_and_tests/config/validator.py](attempts/attempt_4_designer_and_tests/config/validator.py)
   - [attempts/attempt_4_designer_and_tests/config/loader.py](attempts/attempt_4_designer_and_tests/config/loader.py)
   - [attempts/attempt_4_designer_and_tests/configs/classic.json](attempts/attempt_4_designer_and_tests/configs/classic.json), [extended.json](attempts/attempt_4_designer_and_tests/configs/extended.json), [chaos.json](attempts/attempt_4_designer_and_tests/configs/chaos.json), [custom.json](attempts/attempt_4_designer_and_tests/configs/custom.json)

6. **What I Got (Did It Work?):**
   Yes—all 4 presets validated and loaded cleanly, and all 14 invalid/incompatible/malformed configuration cases raised `ConfigValidationError` with exact field and line/column diagnostics.

   Observed verification output:
   ```text
   Loaded preset classic.json: variant=classic, board={'width': 10, 'height': 20}, strategy=bag, renderer=cli
   Loaded preset extended.json: variant=extended, board={'width': 12, 'height': 22}, strategy=adaptive, renderer=cli
   Loaded preset chaos.json: variant=chaos, board={'width': 14, 'height': 24}, strategy=markov, renderer=cli
   Loaded preset custom.json: variant=custom, board={'width': 10, 'height': 20}, strategy=bag, renderer=headless
   Rejected [small_board]: - Invalid board.width=2: must be an integer between 4 and 40.
   Rejected [unknown_variant]: - Unknown variant 'mega_tetris'. Valid options: classic, extended, chaos, custom.
   Rejected [unknown_dist]: - Unknown distribution.strategy 'quantum'. Valid options: uniform, weighted, bag, adaptive, markov.
   Rejected [unknown_renderer]: - Unknown renderer 'sdl'. Valid options: headless, cli, tk.
   Rejected [negative_holes]: - Invalid max_holes=-1: must be null or an integer in 0..6.
   Rejected [bool_holes]: - Invalid max_holes=True: must be null or an integer in 0..6.
   Rejected [too_fast_speed]: - Invalid gameplay.initial_speed_ms=40: must be an integer between 100 and 5000 ms.
   Rejected [bad_seed_type]: - Invalid distribution.seed='abc': must be null or an integer.
   Rejected [bool_seed]: - Invalid distribution.seed=False: must be null or an integer.
   Rejected [unknown_key_typo]: - Unknown top-level key(s): widht.
   Rejected [classic_plus_diagonal]: - Incompatible settings: variant='classic' contains only orthogonal shapes and cannot use connectivity='diagonal'.
   Rejected [negative_weight]: - Invalid weight for piece '1' (-2): weights must be non-negative numbers.
   Rejected [malformed_json]: - Malformed JSON in '.../broken.json' at line 1, column 14: ...
   Rejected [missing_file]: - Configuration file not found: .../missing.json
   ```

7. **How I Got It (Modifications & Independent Research):**
   Explicitly guarded against Python's `isinstance(True, int) == True` pitfall in `_is_strict_int()` so booleans passed to `max_holes` or `seed` are properly rejected rather than treated as `0` or `1`, and combined structural validation with optional `jsonschema` cross-validation.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Human-readable multi-error reporting, zero-dependency core validation (with optional `jsonschema` support), and strict unknown-key rejection.
   - **Weaknesses:** Still needs `ExTetrisBuilder`, variant export, save/load/resume persistence (Prompt 2), and `ExTetris_Studio.ipynb` (Prompt 3).

---

## INT-018 — [Attempt 4] Fluent `ExTetrisBuilder`, Variant Export & Save/Load/Resume Persistence
- **Timestamp:** 2026-11-26 11:37 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   In attempts/attempt_4_designer_and_tests/, implement: (1) the Fluent ExTetrisBuilder API (use_classic_tetris(), use_extended_tetris(), filter_max_holes(n), filter_orthogonal_only(), filter_diagonal_only(), with_board_size(w, h), with_speed(...), with_distribution(...), with_renderer(...), from_json(...), build(), and export_variant(out_dir) to release a configured variant with documentation), and (2) full game-state persistence (save_state(path) / load_state(path) saving board grid, active/next pieces, cursor, score, lines, level, FSM state, and seed so a paused/running game can resume identically, alongside text export). Verify builder chaining, variant export, and save/load/resume
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Implemented `ExTetrisBuilder`, `export_variant()`, and full JSON state persistence in `attempts/attempt_4_designer_and_tests/`:

   ### Files Created / Updated
   * [builder.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/builder.py) — Fluent `ExTetrisBuilder` (`use_classic_tetris()`, `use_extended_tetris()`, `use_chaos_tetris()`, `filter_max_holes()`, `filter_orthogonal_only()`, `filter_diagonal_only()`, `with_board_size()`, `with_speed()`, `with_distribution()`, `with_renderer()`, `from_json()`, `build()`, `export_variant()`) + `load_game_from_json()`.
   * [persistence.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/persistence.py) & [engine.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/engine.py) — `save_state()`, `load_state()`, and `export_text_board()` serializing grid, pieces, cursor, score, lines, level, FSM state, and distribution/RNG state.

   ### Bug Caught & Fixed During Testing
   * Initial save/load/resume parity failed on the 4th move after resuming because `load_engine_state()` passed the deserialized `BagDistribution` into `ExTetrisEngine.__init__()`, whose `_init_pieces()` popped 2 elements off `_bag`. Assigning `engine.distribution` **after** `engine_cls(...)` resolved it cleanly.

   ### Verification Output
   ```text
   1. Fluent ExTetrisBuilder chaining + headless run verified, score = 38
   2. load_game_from_json(configs/custom.json) verified.
   3. Empty filtered pool rejected: - Current variant and filters leave 0 matching ExTetromino shapes.
   4. export_variant() generated config/docs/launcher and ran standalone cleanly, piece_count = 9
   5. Save / Load / Resume bit-identical state & RNG continuation verified!
   6. Corrupt save file rejected: Invalid or unsupported ExTetris state file format.
   ```

   Logged verbatim as `INT-018` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 3** (`ExTetris_Studio.ipynb` no-code interactive studio)!
   ````

3. **What I Interpreted:**
   Game designers need a fluent Python API (`ExTetrisBuilder`) and one-command variant export (`export_variant()` generating config, docs, and a standalone launcher), while players/tests need true state persistence (`save_state`/`load_state`) that restores not just the board grid but also exact piece queue and RNG state.

4. **What I Planned:**
   Implement `persistence.py` serializing board grid, pieces, cursor, FSM state, scoring, and `Distribution` RNG/bag/Markov state; implement `ExTetrisBuilder` with fluent setters, validation, and `export_variant()`; and test both standalone variant execution and resume parity.

5. **What I Implemented:**
   - [attempts/attempt_4_designer_and_tests/persistence.py](attempts/attempt_4_designer_and_tests/persistence.py)
   - [attempts/attempt_4_designer_and_tests/builder.py](attempts/attempt_4_designer_and_tests/builder.py)
   - [attempts/attempt_4_designer_and_tests/engine.py](attempts/attempt_4_designer_and_tests/engine.py) (`save_state`, `load_state`, `export_text_board`)

6. **What I Got (Did It Work?):**
   Yes—after fixing the post-`__init__` distribution restoration order in `persistence.py`, fluent builder chaining, `from_json`, empty-pool rejection, standalone `export_variant()` execution (`9` pieces), bit-identical save/load/resume parity, and corrupt-save rejection all passed (`exit code 0`).

7. **How I Got It (Modifications & Independent Research):**
   - Diagnosed the exact bag-length divergence (`[28, 35, 48, 29, 49, 26]` vs `[28, 35, 48, 29]`) by printing `sim_eng.distribution._bag` vs `restored.distribution._bag` right after `load_state()`. Passing `distribution=None` into `engine_cls(...)` and assigning `engine.distribution` afterward prevented `_init_pieces()` from consuming restored bag/RNG state.
   - Embedded `ENGINE_DIR` fallback into the generated `run_variant.py` so exported variants run from any output directory.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** One-call variant release with auto-generated documentation; bit-identical save/load/resume across RNG/bag state; clean fluent API.
   - **Weaknesses:** Still needs `ExTetris_Studio.ipynb` for interactive no-code design (Prompt 3) and the categorized test suite (Prompt 4).

---

## INT-019 — [Attempt 4] No-Code `ExTetris_Studio.ipynb` & Variant Launcher
- **Timestamp:** 2026-11-26 11:40 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Create ExTetris_Studio.ipynb in attempts/attempt_4_designer_and_tests/ wired directly to config/loader.py and ExTetrisBuilder (no duplicated game rules). Demonstrate a complete no-code workflow: inspecting the 110 shapes by bounding box/morphology/landing holes, adjusting variant settings (board size, distribution, max holes, connectivity, speed) via interactive widgets / JSON config, previewing sampled distributions, exporting a standalone variant JSON + documentation, and launching a headless simulation or GUI/CLI session without editing Python source. Execute the notebook non-interactively to verify every code cell runs cleanly.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Created [ExTetris_Studio.ipynb](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb) and [play.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/play.py) in `attempts/attempt_4_designer_and_tests/`, wired directly to `config/` and `ExTetrisBuilder`:

   ### What Was Implemented
   * **[ExTetris_Studio.ipynb](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb) (6 executable code cells):**
     1. Setup & imports from `config` and `builder` (zero duplicated game rules).
     2. Catalog inspection across all 110 shapes, bounding boxes (including `3×4` and `4×3`), and landing holes.
     3. `ipywidgets` interactive variant configurator (`Variant`, `Scope`, `Connect`, `Max Holes`, `Width`, `Height`, `Dist`, `Speed`) backed by `validate_config()`.
     4. Live invalid-configuration demo (`ConfigValidationError` on `width=2` and `classic`+`diagonal`).
     5. Filtered pool & distribution sampling preview (`16` diagonal shapes with `<=3` holes).
     6. Standalone `export_variant()` test + subprocess launcher verification + 12-step headless simulation (`Score=34`).
   * **[play.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/play.py):** CLI/GUI launcher supporting `--config`, `--renderer`, `--seed`, and `--steps`.

   ### Verification Output
   * Executed `jupyter nbconvert --to notebook --execute --inplace ExTetris_Studio.ipynb`: all 6 code cells (`exec_count=1..6`) passed cleanly (`51,091` bytes written).
   * Executed `python3 play.py --config configs/custom.json --steps 8`: passed (`Captured 9 headless frames. Final score=0, state=RUNNING`).

   Logged verbatim as `INT-019` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 4** (full categorized test suite in `attempts/attempt_4_designer_and_tests/tests/`)!
   ````

3. **What I Interpreted:**
   PDF Section 3 explicitly draws an analogy to Jupyter notebooks empowering non-programmers. `ExTetris_Studio.ipynb` must act as a true no-code studio backed 100% by `config/` and `ExTetrisBuilder` without duplicating any game rules.

4. **What I Planned:**
   Author a 6-code-cell notebook covering catalog inspection, `ipywidgets` variant controls + live validation, invalid-config rejection demo, distribution sampling preview, standalone variant export + subprocess run, and headless simulation; verify non-interactive execution via `nbconvert`; and add `play.py --config`.

5. **What I Implemented:**
   - [attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb](attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb)
   - [attempts/attempt_4_designer_and_tests/play.py](attempts/attempt_4_designer_and_tests/play.py)

6. **What I Got (Did It Work?):**
   Yes—`jupyter nbconvert --execute` ran all 6 code cells (`exec_count=1..6`) with zero cell errors and populated outputs (`51,091` bytes), and `play.py --config configs/custom.json` launches configured variants directly.

   Observed notebook execution output:
   ```text
   [NbConvertApp] Writing 51091 bytes to ExTetris_Studio.ipynb
   Cell 1 (exec_count=1): Loaded ExTetris Studio from: .../attempts/attempt_4_designer_and_tests
   Cell 3 (exec_count=2): Catalog Summary (110 fixed, 34 one-sided, 22 free), 3x4 Diagonal ID 78 preview
   Cell 5 (exec_count=3): Active validated studio_config: Studio Custom Diagonal Variant | board= {'width': 12, 'height': 20} | strategy= adaptive
   Cell 7 (exec_count=4): Rejected invalid width=2 and classic+diagonal conflict via ConfigValidationError
   Cell 9 (exec_count=5): Filtered pool size: 16 shapes (all diagonal=True, max_holes<=3), sampled 30 pieces
   Cell 11 (exec_count=6): Exported variant_config.json, VARIANT_README.md, run_variant.py; standalone launcher & 12-step headless sim (Score=34) passed
   ```

7. **How I Got It (Modifications & Independent Research):**
   An initial inline command hit shell backtick/quote escaping issues when generating the notebook; switched to a single-quoted heredoc (`cat << 'EOF' | python3`) so notebook strings serialized cleanly before `nbconvert` execution.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** True no-code variant studio using a single validation/builder source of truth; works both interactively with `ipywidgets` and deterministically in headless `nbconvert`.
   - **Weaknesses:** Still needs the full categorized test suite under `tests/` (Prompt 4) to verify all 9 categories together.

---

## INT-020 — [Attempt 4] Categorized Test Suite Across All Functional Areas
- **Timestamp:** 2026-11-26 11:41 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Build a comprehensive categorized test suite in attempts/attempt_4_designer_and_tests/tests/ covering: (1) Shape generation, (2) Shape hierarchy, (3) Board, (4) Rotations & wall kicks, (5) Seeded distributions & combinators, (6) Engine FSM & scoring, (7) Configuration (valid presets, Builder, and invalid-configuration error cases), (8) Persistence (save, load, resume), and (9) Integration (CLI, Headless, optional Tkinter, and Notebook workflow). Run the full suite, fix any bugs uncovered, and show exact test counts and runtimes
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Built and executed the categorized test suite under `attempts/attempt_4_designer_and_tests/tests/` covering all 9 functional areas:

   ### Test Categories Added
   * [test_generation_and_hierarchy.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_shapes/test_generation_and_hierarchy.py) — 110 unique shapes, connectivity, normalization, all 11 bounding boxes (incl. `3×4` & `4×3`), morphology, landing-hole profiles, invalid invariants
   * [test_board.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_board/test_board.py) — Negative indices, boundaries, collisions, line clearing, hole/height/bumpiness metrics
   * [test_rotations_and_wallkicks.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_rotations/test_rotations_and_wallkicks.py) — 4 rotations across all 110 shapes, CW/CCW wall kicks, blocked & disabled kick rejections
   * [test_distributions.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_distributions/test_distributions.py) — Seeded Uniform, Weighted, Bag, Markov, Adaptive, and `.filter`/`.map`/`.blend`/`+`/`>>`/`.conditional` combinators
   * [test_engine_fsm.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_engine/test_engine_fsm.py) — FSM lifecycle, Observer callbacks, level progression, speed rounding & `100ms` floor
   * [test_config_and_builder.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_configuration/test_config_and_builder.py) — All 4 JSON presets, invalid/malformed config errors, fluent Builder chaining, `export_variant()`
   * [test_persistence.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_persistence/test_persistence.py) — JSON save/load/bit-identical resume, text board export, corrupt/missing file errors
   * [test_integration.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/tests/test_integration/test_integration.py) — Headless, CLI, `play.main("--config", ...)`, optional Tkinter, and headless `jupyter nbconvert` execution of `ExTetris_Studio.ipynb`

   ### Exact Test Output
   *(Initial run hit 1 fixture failure in `test_wall_kicks_and_invalid_rotations` because row `10` was blocked instead of row `8` where the rotated `1×4` piece sits; after fixing the fixture row to `8`, all 22 tests passed.)*

   ```text
   Ran 22 tests in 6.638s

   OK
   ```

   Logged verbatim as `INT-020` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 5** (audit Attempt 4, write `ATTEMPT_4_REPORT.md`, commit, and tag `attempt-4-designer-and-tests`)!
   ````

3. **What I Interpreted:**
   All Attempt 4 subsystems—shape generation/hierarchy, board, rotations/wall kicks, seeded distributions, FSM engine, config validation/Builder, state persistence, and CLI/Headless/Tk/Notebook workflows—needed to be organized into clear test categories and verified in one run.

4. **What I Planned:**
   Create modular `unittest` files under `tests/test_*/` covering every category, including invalid-configuration rejection, bit-identical save/load/resume, and headless `nbconvert` notebook execution, then run the full discovery suite.

5. **What I Implemented:**
   - `attempts/attempt_4_designer_and_tests/tests/test_shapes/test_generation_and_hierarchy.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_board/test_board.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_rotations/test_rotations_and_wallkicks.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_distributions/test_distributions.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_engine/test_engine_fsm.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_configuration/test_config_and_builder.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_persistence/test_persistence.py`
   - `attempts/attempt_4_designer_and_tests/tests/test_integration/test_integration.py`

6. **What I Got (Did It Work?):**
   Yes—after fixing the obstacle row in `test_wall_kicks_and_invalid_rotations`, all **22 tests passed in `6.638s` (`OK`)**, including live notebook execution via `jupyter nbconvert`.

7. **How I Got It (Modifications & Independent Research):**
   Diagnosed `AssertionError: True is not false` on `eng.rotate_cw()` at `cursor = (8, 5)`: a `4×1` vertical piece at `(8, 5)` occupies rows `8..11`, and when rotated CW to `1×4` horizontal, it lies entirely on row `8`, so blocking row `10` did not block the rotation. Moving the single-gap wall (`area[8, :] = True; area[8, 5] = False`) properly forced every kick offset `(0, ±1, ±2)` to collide.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Comprehensive categorized suite covering valid, invalid-config, persistence, and end-to-end notebook/CLI integration in under 7 seconds.
   - **Weaknesses:** Still lives inside `attempts/attempt_4_designer_and_tests/`; needs promotion to the root `extetris/` package, `Makefile`/shell scripts, `test_packaging/` clean-venv verification, and final `docs/` in Attempt 5.

---

## INT-021 — [Attempt 4] Audit Attempt 4, Write Report, Commit & Tag
- **Timestamp:** 2026-11-26 11:43 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Audit attempts/attempt_4_designer_and_tests/ against all assignment requirements to list what Attempt 4 completed and what remains for Attempt 5 (promoting the clean modular package to root extetris/, adding Makefile/setup.sh/run.sh/test.sh, clean-environment packaging verification in tests/test_packaging/, and finalizing docs/). Write attempts/attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md, update AI_INTERACTION_LOG.md, commit Attempt 4, tag it attempt-4-designer-and-tests, and update attempts/README.md
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   **Attempt 4 (Designer Interface, Validation, Persistence & Categorized Tests)** is complete, verified, and tagged in Git.

   ### Summary of Deliverables
   * **Report:** [ATTEMPT_4_REPORT.md](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md)
   * **Snapshot (`attempts/attempt_4_designer_and_tests/`):**
     * Config & presets: [schema.json](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/config/schema.json), [validator.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/config/validator.py), [loader.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/config/loader.py), `configs/{classic,extended,chaos,custom}.json`
     * Builder, launcher & persistence: [builder.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/builder.py), [persistence.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/persistence.py), [play.py](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/play.py)
     * No-code Studio: [ExTetris_Studio.ipynb](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb) (6 code cells executed cleanly via `nbconvert`)
     * Categorized test suite: `tests/` (**22/22 tests passing in `6.638s`**)
   * **Logs & Index:**
     * [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md) updated (`INT-017` through `INT-021`)
     * [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md) updated (`c18c89a`, tag `attempt-4-designer-and-tests`, index commit `49a73f5`)

   Ready whenever you want to move on to **Attempt 5 (Final Root Package, Build Automation, Clean-Environment Packaging Test & Complete Docs)**—I can also provide the Attempt 5 prompt sequence if you'd like!
   ````

3. **What I Interpreted:**
   With the designer layer, validation, persistence, notebook, and 22 categorized tests passing, we need a clear boundary audit separating Attempt 4's completed functionality from Attempt 5's packaging, build scripts, clean-venv verification, and final documentation.

4. **What I Planned:**
   Run file/line audit across `attempts/attempt_4_designer_and_tests/`, write `ATTEMPT_4_REPORT.md`, log `INT-021`, commit and tag `attempt-4-designer-and-tests`, and record the commit hash in `attempts/README.md`.

5. **What I Implemented:**
   - [attempts/attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md](attempts/attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md).

6. **What I Got (Did It Work?):**
   Yes—Attempt 4 snapshot committed cleanly, tagged `attempt-4-designer-and-tests`, and indexed in `attempts/README.md`.

7. **How I Got It (Modifications & Independent Research):**
   Verified every file under `attempts/attempt_4_designer_and_tests/` excluding `__pycache__` and `.ipynb_checkpoints` before committing.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** End-to-end designer workflow (`JSON` + `ExTetrisBuilder` + `ExTetris_Studio.ipynb` + `save/load/resume` + `22/22` tests) works self-contained inside `attempts/attempt_4_designer_and_tests/`.
   - **Weaknesses:** Needs final package promotion to root `extetris/`, `Makefile`/shell scripts, clean-venv packaging test, and final `docs/` in Attempt 5.

---

## INT-022 — [Attempt 5] Promote Modular `extetris/` Package, Root `configs/`, and Root `ExTetris_Studio.ipynb`
- **Timestamp:** 2026-11-26 11:52 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Promote the verified Attempt 4 codebase into the clean modular package at the repository root: extetris/ (shapes/, board/, distributions/, engine/, renderers/, config/, builder.py, cli.py), root configs/ (classic.json, extended.json, chaos.json, custom.json), and root ExTetris_Studio.ipynb (updated to import from extetris directly). Verify pip install -e . (or python3 -m extetris.cli), pyproject.toml entrypoint extetris, and execute the root ExTetris_Studio.ipynb cleanly.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Promoted the codebase into the modular root `extetris/` package, populated root `configs/`, updated and executed root `ExTetris_Studio.ipynb`, and verified package installation and CLI entrypoints:

   ### Files Created / Updated
   * **Modular Package (`extetris/`):**
     * [extetris/__init__.py](file:///Users/vanshsharma/Documents/POPL/extetris/__init__.py)
     * `shapes/`: [base.py](file:///Users/vanshsharma/Documents/POPL/extetris/shapes/base.py), [hierarchy.py](file:///Users/vanshsharma/Documents/POPL/extetris/shapes/hierarchy.py), [factory.py](file:///Users/vanshsharma/Documents/POPL/extetris/shapes/factory.py)
     * `board/`: [board.py](file:///Users/vanshsharma/Documents/POPL/extetris/board/board.py)
     * `distributions/`: [distributions.py](file:///Users/vanshsharma/Documents/POPL/extetris/distributions/distributions.py)
     * `engine/`: [engine.py](file:///Users/vanshsharma/Documents/POPL/extetris/engine/engine.py), [persistence.py](file:///Users/vanshsharma/Documents/POPL/extetris/engine/persistence.py)
     * `renderers/`: [renderers.py](file:///Users/vanshsharma/Documents/POPL/extetris/renderers/renderers.py)
     * `config/`: [schema.json](file:///Users/vanshsharma/Documents/POPL/extetris/config/schema.json), [validator.py](file:///Users/vanshsharma/Documents/POPL/extetris/config/validator.py), [loader.py](file:///Users/vanshsharma/Documents/POPL/extetris/config/loader.py)
     * [builder.py](file:///Users/vanshsharma/Documents/POPL/extetris/builder.py) & [cli.py](file:///Users/vanshsharma/Documents/POPL/extetris/cli.py)
   * **Root Presets & Studio:** [configs/classic.json](file:///Users/vanshsharma/Documents/POPL/configs/classic.json), [extended.json](file:///Users/vanshsharma/Documents/POPL/configs/extended.json), [chaos.json](file:///Users/vanshsharma/Documents/POPL/configs/chaos.json), [custom.json](file:///Users/vanshsharma/Documents/POPL/configs/custom.json), and [ExTetris_Studio.ipynb](file:///Users/vanshsharma/Documents/POPL/ExTetris_Studio.ipynb)

   ### Verification Output
   * `jupyter nbconvert --to notebook --execute --inplace ExTetris_Studio.ipynb`: executed all 6 code cells cleanly (`50,770` bytes written).
   * `python3 -m pip install --no-build-isolation --no-deps -e .`: built and installed `extetris-0.1.0` cleanly.
   * `extetris --config configs/custom.json --steps 8` and `python3 -m extetris.cli --variant extended --renderer headless --seed 42 --steps 8`: both exited `0` (`Captured 9 headless frames`).

   Logged verbatim as `INT-022` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 2** (`Makefile`, `setup.sh`, `run.sh`, `test.sh`, root `tests/`, and `make package`)!
   ````

3. **What I Interpreted:**
   To ship Attempt 5 as a clean, installable Python package matching `pyproject.toml`, Attempt 4's modules had to be refactored into modular subpackages (`extetris.shapes`, `extetris.board`, `extetris.distributions`, `extetris.engine`, `extetris.renderers`, `extetris.config`) with proper relative/package imports and a console entrypoint.

4. **What I Planned:**
   Organize `extetris/` subpackages and `__init__.py` re-exports, add `extetris/cli.py`, copy the 4 JSON presets into `configs/`, update `ExTetris_Studio.ipynb` to import directly from `extetris`, run `nbconvert --execute`, run `pip install --no-build-isolation --no-deps -e .`, and test both CLI invocations.

5. **What I Implemented:**
   - `extetris/__init__.py`, `shapes/{__init__.py,base.py,hierarchy.py,factory.py}`, `board/{__init__.py,board.py}`, `distributions/{__init__.py,distributions.py}`, `engine/{__init__.py,engine.py,persistence.py}`, `renderers/{__init__.py,renderers.py}`, `config/{__init__.py,schema.json,validator.py,loader.py}`, `builder.py`, `cli.py`
   - `configs/{classic,extended,chaos,custom}.json`
   - `ExTetris_Studio.ipynb`

6. **What I Got (Did It Work?):**
   Yes—`ExTetris_Studio.ipynb` executed cleanly (`50,770` bytes), `extetris-0.1.0` installed cleanly via `pyproject.toml`, and both `extetris` and `python3 -m extetris.cli` ran headless simulations cleanly.

   Observed verification output:
   ```text
   [NbConvertApp] Writing 50770 bytes to ExTetris_Studio.ipynb
   Successfully built extetris
   Installing collected packages: extetris
   Successfully installed extetris-0.1.0
   extetris --config configs/custom.json --steps 8 -> Captured 9 headless frames. Final score=0, state=RUNNING
   python3 -m extetris.cli --variant extended --renderer headless --seed 42 --steps 8 -> Captured 9 headless frames. Final score=0, state=RUNNING
   ```

7. **How I Got It (Modifications & Independent Research):**
   Updated `ExTetrisBuilder.export_variant()` so the generated `run_variant.py` tries `from extetris import load_game_from_json` first (for clean venv installs) and falls back to adding `REPO_ROOT` to `sys.path` when launched uninstalled from a source checkout.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Clean installable Python package layout, console entrypoint, single source of truth across CLI, Builder, and Notebook.
   - **Weaknesses:** Still needs root `Makefile`/shell scripts, root `tests/`, clean-venv packaging test (`tests/test_packaging/`), and final `docs/` (Prompts 2–5).

---

## INT-023 — [Attempt 5] Build Automation, Root Tests & Submission ZIP Packaging
- **Timestamp:** 2026-11-26 11:57 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Create Makefile (targets: setup, run, run-classic, run-extended, run-chaos, run-gui, test, package, clean), setup.sh, run.sh, and test.sh at the repository root, and promote all 8 categorized test suites into root tests/ using the extetris package. Ensure make package builds dist/extetris_submission.zip containing the package, configs/, tests/, ExTetris_Studio.ipynb, docs/, attempts/, AI_INTERACTION_LOG.md, scripts, LICENSE, README.md, and pyproject.toml (excluding .git/, .venv/, __pycache__/, dist/, and private drafts). Run test.sh and make package and verify.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   [Intermediate Status Update 1 — Verbatim]
   Launched `./test.sh`, `make package`, and the ZIP/runner verification checks; waiting for the background command to finish.

   [Final Assistant Response — Verbatim]
   Created the root build/run scripts, `extetris/packaging.py`, and promoted all 8 categorized test modules into root `tests/`:

   ### Files Created
   * Build & scripts: [Makefile](file:///Users/vanshsharma/Documents/POPL/Makefile) (`setup`, `run`, `run-classic`, `run-extended`, `run-chaos`, `run-gui`, `test`, `package`, `clean`), [setup.sh](file:///Users/vanshsharma/Documents/POPL/setup.sh), [run.sh](file:///Users/vanshsharma/Documents/POPL/run.sh), [test.sh](file:///Users/vanshsharma/Documents/POPL/test.sh)
   * Packager: [extetris/packaging.py](file:///Users/vanshsharma/Documents/POPL/extetris/packaging.py) *(extracted out of Make after Make's backslash line-continuation turned an inline Python block into a `SyntaxError`)*
   * Root tests: `tests/test_{shapes,board,rotations,distributions,engine,configuration,persistence,integration}/` importing directly from `extetris`

   ### Verification Output
   * `./test.sh` (`pytest`): **22 passed in 8.64s**.
   * `make package`: Created `dist/extetris_submission.zip` (**123 files**, `207,402` bytes) with all required files present and `.git/`, `.venv/`, `__pycache__/`, `dist/`, and private drafts excluded.
   * `./run.sh --config configs/custom.json --steps 5`: Passed (`Captured 6 headless frames. Final score=0, state=RUNNING`).

   Logged verbatim as `INT-023` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 3** (`tests/test_packaging/test_submission_package.py` clean-venv verification)!
   ````

3. **What I Interpreted:**
   To satisfy PDF Section 3's build/run script requirement and clean packaging, root automation (`Makefile`, `setup.sh`, `run.sh`, `test.sh`) must work cross-platform and exclude transient caches, `.git`, `.venv`, `dist`, and private draft files from `extetris_submission.zip`.

4. **What I Planned:**
   Write `Makefile` with all 9 targets, executable shell wrappers (`setup.sh`, `run.sh`, `test.sh`), `extetris/packaging.py` for clean ZIP generation, and promote all 8 test suites under `tests/test_*/` to test the installed `extetris` package.

5. **What I Implemented:**
   - [Makefile](Makefile), [setup.sh](setup.sh), [run.sh](run.sh), [test.sh](test.sh)
   - [extetris/packaging.py](extetris/packaging.py)
   - Root test modules under `tests/test_shapes/`, `test_board/`, `test_rotations/`, `test_distributions/`, `test_engine/`, `test_configuration/`, `test_persistence/`, `test_integration/`.

6. **What I Got (Did It Work?):**
   Yes—`./test.sh` passed **22/22 tests in `8.64s`**, `make package` generated a clean **123-file** `dist/extetris_submission.zip` (`207,402` bytes) with zero excluded paths, and `./run.sh` launched the configured variant cleanly.

7. **How I Got It (Modifications & Independent Research):**
   - Replaced the inline Make `python3 -c` block with `extetris/packaging.py` (`$(PYTHON) -m extetris.packaging`) after Make's backslash line-continuation turned multi-line Python blocks into a `SyntaxError`.
   - Guarded `test_notebook_workflow_executes_cleanly` with `importlib.util.find_spec("nbconvert")` so minimal virtual environments without Jupyter skip only the optional notebook execution check while full dev environments run it.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Portable Python-based ZIP packaging, single-command `make` targets, clean root test suite.
   - **Weaknesses:** Still needs `tests/test_packaging/` clean-venv verification (Prompt 3) and complete `docs/` (Prompts 4–5).

---

## INT-024 — [Attempt 5] Clean-Environment Packaging Verification (`tests/test_packaging/`)
- **Timestamp:** 2026-11-26 11:59 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Implement tests/test_packaging/test_submission_package.py to verify the release from a clean environment: (1) build dist/extetris_submission.zip, (2) extract it into a temporary directory, (3) create a clean virtual environment (python3 -m venv) and pip install the extracted project, (4) run the full unit/integration test suite inside the clean venv (skipping recursive packaging), (5) launch a basic game variant via the installed extetris CLI, and (6) load and validate a JSON configuration from configs/. Run the complete root pytest / unittest suite including test_packaging/ and report exact counts and runtimes
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   [Intermediate Status Update 1 — Verbatim]
   Running `./test.sh` (including the clean-venv packaging verification in `tests/test_packaging/test_submission_package.py`); waiting for it to finish.

   [Final Assistant Response — Verbatim]
   Implemented [test_submission_package.py](file:///Users/vanshsharma/Documents/POPL/tests/test_packaging/test_submission_package.py) and verified the full packaged release from a clean virtual environment.

   ### What Was Verified in `test_clean_venv_install_tests_cli_and_config`
   1. Built `extetris_submission.zip` via `build_submission_zip()`.
   2. Extracted the archive into a fresh temporary directory.
   3. Created an isolated `python3 -m venv` (with `PYTHONPATH` stripped) and ran `pip install`.
   4. Executed `unittest discover` inside the clean venv (`EXTETRIS_SKIP_PACKAGING_TEST=1`).
   5. Launched `extetris --config configs/custom.json --steps 6` via the installed console entrypoint.
   6. Loaded & validated `configs/extended.json` from outside the extracted tree, confirming `extetris.__file__` resolved inside the temp venv.

   ### Exact Test Output (`./test.sh`)
   ```text
   ============================= 23 passed in 38.86s ==============================
   ```

   Logged verbatim as `INT-024` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 4** (`docs/DESIGN.md`, `docs/UML.md`, `docs/API.md`, `docs/GAME_PROGRAMMERS_MANUAL.md`, and root `README.md`)!
   ````

3. **What I Interpreted:**
   To prove the packaged ZIP works independently of our local development setup (not just via editable installs or `PYTHONPATH`), we must test building the ZIP, extracting it, installing into a fresh `python3 -m venv` with `PYTHONPATH` stripped, running the tests, invoking the installed `extetris` binary, and validating JSON configs from outside the extracted tree.

4. **What I Planned:**
   Write `TestSubmissionPackage.test_clean_venv_install_tests_cli_and_config` guarding against recursion via `EXTETRIS_SKIP_PACKAGING_TEST=1`, stripping `PYTHONPATH`/`PYTHONHOME`/`VIRTUAL_ENV`, running `pip install`, `unittest discover`, `extetris --config configs/custom.json --steps 6`, and `extetris.load_config(...)` asserting `extetris.__file__` resolves inside the temp venv.

5. **What I Implemented:**
   - [tests/test_packaging/test_submission_package.py](tests/test_packaging/test_submission_package.py)

6. **What I Got (Did It Work?):**
   Yes—all **23 tests passed in `38.86s`** on the first run (`./test.sh`), proving the packaged submission installs and runs cleanly in an isolated virtual environment.

   Observed output:
   ```text
   tests/test_packaging/test_submission_package.py::TestSubmissionPackage::test_clean_venv_install_tests_cli_and_config PASSED [ 65%]
   ...
   ============================= 23 passed in 38.86s ==============================
   ```

7. **How I Got It (Modifications & Independent Research):**
   Verified via `extetris.__file__` path assertion from `cwd=tmp_path` (outside `extract_dir`) that Python truly imported `extetris` from the fresh venv's `site-packages` rather than the working directory.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Genuine end-to-end release validation from archive build through isolated venv execution.
   - **Weaknesses:** Still needs the complete `docs/` suite (`DESIGN.md`, `UML.md`, `API.md`, `GAME_PROGRAMMERS_MANUAL.md`, `AI_USAGE_REPORT.md`) and final `attempt-5-final` tag (Prompts 4–5).

---

## INT-025 — [Attempt 5] Technical Design, UML, API & Game Programmer's Manual
- **Timestamp:** 2026-11-26 12:01 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Author the complete technical and designer documentation under docs/ aligned strictly with the actual extetris/ implementation: (1) docs/DESIGN.md (architecture, division of labour, entity-relationships, and design decisions), (2) docs/UML.md (Mermaid class diagram, 4-state FSM diagram, and gameplay/distribution sequence diagram), (3) docs/API.md (Application Programmer's Manual covering all public classes and methods), and (4) docs/GAME_PROGRAMMERS_MANUAL.md (non-technical step-by-step guide for designing and releasing ExTetris variants via JSON, ExTetris_Studio.ipynb, and export_variant without programming expertise). Update root README.md with clear quickstart and doc links.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   Authored the technical and designer documentation under `docs/` and updated root [README.md](file:///Users/vanshsharma/Documents/POPL/README.md):

   ### Files Created / Updated
   * [docs/DESIGN.md](file:///Users/vanshsharma/Documents/POPL/docs/DESIGN.md) — 6-layer architecture, division of labour, coordinate representation, multi-axis subclass synthesis, Functional-OO distress formula, UI decoupling, and persistence design.
   * [docs/UML.md](file:///Users/vanshsharma/Documents/POPL/docs/UML.md) — Mermaid class diagram, 4-state FSM diagram (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), and variant assembly/gameplay sequence diagram.
   * [docs/API.md](file:///Users/vanshsharma/Documents/POPL/docs/API.md) — Application Programmer's Manual documenting all public classes and methods across `extetris.*`.
   * [docs/GAME_PROGRAMMERS_MANUAL.md](file:///Users/vanshsharma/Documents/POPL/docs/GAME_PROGRAMMERS_MANUAL.md) — Non-programmer step-by-step guide covering presets, `ExTetris_Studio.ipynb`, JSON configuration editing, and standalone variant export.
   * [README.md](file:///Users/vanshsharma/Documents/POPL/README.md) — Quickstart, feature overview, and clickable doc links.

   ### Verification
   * Verified `./run.sh --config configs/custom.json --export /tmp/test_cli_export && python3 /tmp/test_cli_export/run_variant.py` executed cleanly (`Exported variant (9 shapes)...`).

   Logged verbatim as `INT-025` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md). Ready for **Prompt 5** (`docs/AI_USAGE_REPORT.md`, final ZIP rebuild, final test run, Git commit, and `attempt-5-final` tag)!
   ````

3. **What I Interpreted:**
   Section 3.1 stresses documentation as the most important part, requiring both technical artifacts (Design + UML + API Reference) and an accessible Game Programmer's Manual for non-coders.

4. **What I Planned:**
   Write `DESIGN.md` (6-layer division of labour & architectural decisions), `UML.md` (Mermaid class, state, and sequence diagrams), `API.md` (all public exports across `extetris.*`), `GAME_PROGRAMMERS_MANUAL.md` (presets, Jupyter Studio, JSON editing, variant export), and update `README.md`.

5. **What I Implemented:**
   - [docs/DESIGN.md](docs/DESIGN.md)
   - [docs/UML.md](docs/UML.md)
   - [docs/API.md](docs/API.md)
   - [docs/GAME_PROGRAMMERS_MANUAL.md](docs/GAME_PROGRAMMERS_MANUAL.md)
   - [README.md](README.md)

6. **What I Got (Did It Work?):**
   Yes—all four documentation files and `README.md` match the actual codebase symbols and counts, and the documented CLI `--export` + `run_variant.py` workflow ran cleanly (`exit code 0`).

7. **How I Got It (Modifications & Independent Research):**
   Cross-checked every documented symbol, config key, bounding-box class (`Box1x4Shape`..`Box4x4Shape` including `Box3x4Shape` and `Box4x3Shape`), and CLI flag directly against `extetris/` source files and verified the `--export` command in `/tmp`.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Complete separation of audience-specific documentation (architecture/UML/API for developers vs. plain manual for game designers).
   - **Weaknesses:** Still needs `docs/AI_USAGE_REPORT.md` synthesis, final ZIP rebuild, final test run, and `attempt-5-final` tag (Prompt 5).

---

## INT-026 — [Attempt 5] Final `AI_USAGE_REPORT.md`, Packaging, Test Run & Tag `attempt-5-final`
- **Timestamp:** 2026-11-26 12:03 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Write docs/AI_USAGE_REPORT.md synthesizing the full Continued Development Report across Attempts 0–5, referencing exact INT-001..INT-xxx IDs in AI_INTERACTION_LOG.md, summarizing every earlier attempt (including real bugs caught and fixed), and providing a candid effort comparison (actual effort with AI vs. estimated effort without AI). Re-build dist/extetris_submission.zip, re-run the full test suite including test_packaging/, commit Attempt 5 to Git, tag attempt-5-final, and update attempts/README.md.
   ```

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   [Intermediate Status Update 1 — Verbatim]
   Rebuilding `dist/extetris_submission.zip` and running the full 23-test suite (`./test.sh`); waiting for it to finish.

   [Intermediate Status Update 2 — Verbatim]
   Committed `attempts/README.md`, tagged `attempt-5-final`, rebuilt `dist/extetris_submission.zip`, and running the final `./test.sh` verification; waiting for it to finish.

   [Final Assistant Response — Verbatim]
   **Attempt 5 (Final Release)** is complete, verified, packaged, and tagged `attempt-5-final` in Git.

   ### Summary of Deliverables
   * **Master Continued Development & AI Usage Report:** [docs/AI_USAGE_REPORT.md](file:///Users/vanshsharma/Documents/POPL/docs/AI_USAGE_REPORT.md) (synthesizing Attempts 0–5, referencing `INT-001`–`INT-026` in [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md), documenting real bugs caught & fixed, and comparing effort with vs. without AI)
   * **Complete Technical & Designer Docs:**
     * [docs/DESIGN.md](file:///Users/vanshsharma/Documents/POPL/docs/DESIGN.md)
     * [docs/UML.md](file:///Users/vanshsharma/Documents/POPL/docs/UML.md)
     * [docs/API.md](file:///Users/vanshsharma/Documents/POPL/docs/API.md)
     * [docs/GAME_PROGRAMMERS_MANUAL.md](file:///Users/vanshsharma/Documents/POPL/docs/GAME_PROGRAMMERS_MANUAL.md)
     * [README.md](file:///Users/vanshsharma/Documents/POPL/README.md)
   * **Packaged Release & Git History:**
     * `dist/extetris_submission.zip` (**124 files**, `227,727` bytes)
     * Updated [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md) (`3d59b1c`, index commit `4e9ee54`, tag `attempt-5-final`)
     * All 6 tags present: `attempt-0-baseline`, `attempt-1-naive-oop`, `attempt-2-shape-hierarchy`, `attempt-3-engine-and-distributions`, `attempt-4-designer-and-tests`, `attempt-5-final`

   ### Final Verification Output
   * `./test.sh` (`pytest tests -v`, covering all 9 categories including `tests/test_packaging/test_submission_package.py` clean-venv install/test/CLI/config check):
     ```text
     ============================= 23 passed in 22.19s ==============================
     ```
   * `git status -s`: clean working tree.
   ````

3. **What I Interpreted:**
   This final step brings together the master Continued Development Report (Section 2.2), verifies the complete deliverable bundle from a clean environment after all documentation edits, and freezes Attempt 5 in Git as `attempt-5-final`.

4. **What I Planned:**
   Write `docs/AI_USAGE_REPORT.md`, log `INT-026`, rebuild `dist/extetris_submission.zip` via `make package`, run `./test.sh` (`23` tests including `test_packaging/`), commit to Git, tag `attempt-5-final`, and record the final commit hash in `attempts/README.md`.

5. **What I Implemented:**
   - [docs/AI_USAGE_REPORT.md](docs/AI_USAGE_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md)
   - Rebuilt `dist/extetris_submission.zip`

6. **What I Got (Did It Work?):**
   Yes—`make package` produced `dist/extetris_submission.zip` (`124 files, 227708 bytes`) and `./test.sh` passed **23 passed in `24.70s`** (including clean-venv `test_submission_package.py` and live `nbconvert` notebook execution).

7. **How I Got It (Modifications & Independent Research):**
   Confirmed all interaction IDs (`INT-001`..`INT-026`), Git commit hashes/tags (`attempt-0-baseline`..`attempt-4-designer-and-tests`), and observed timings in `AI_USAGE_REPORT.md` match the actual recorded tool outputs.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Complete, reproducible, cleanly packaged submission preserving every historical attempt alongside full technical, API, UML, and non-programmer manuals.
   - **Weaknesses:** Requires internet or cached PyPI wheels during `test_submission_package.py` if run in a strictly offline environment without local wheel cache.

---

## INT-027 — [Attempt 5] Final Specification Audit & Portability Fixes
- **Timestamp:** 2026-11-26 12:47 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ````text
   # Final Improvement Prompt — ExTetris PoPL Assignment

   I want you to thoroughly review and improve the existing ZIP 1 project to make it as strong as possible against the original assignment specification.

   **IMPORTANT: Follow the professor's assignment PDF as the single source of truth. Do not introduce additional features, unnecessary complexity, or requirements that the professor has not asked for.**

   ## 1. Permission and scope rules

   Before starting, read the complete assignment PDF and inspect the existing project.

   Follow these rules strictly:

   1. Do not deviate from the assignment requirements or the existing development plan.
   2. Do not add features simply because they might make the project more impressive.
   3. Do not unnecessarily redesign or rewrite working components.
   4. If you believe a change is necessary that goes beyond the assignment, changes the agreed development plan, or introduces a different approach, **stop and ask for my explicit permission before implementing it.**
   5. Briefly explain why the proposed deviation is necessary and what alternatives exist.
   6. Do not proceed with that change until I approve it.

   You have permission to make normal bug fixes, improve correctness, and improve documentation and testing where they directly support the assignment requirements.

   ## 2. Most important: Continued Development Report

   The professor explicitly states that the continued development report is MORE IMPORTANT than the final outcome.

   Preserve all existing attempts, including unsuccessful and less successful ones.

   Do not delete, overwrite, or artificially improve historical attempts.

   Review:

   - `attempts/`
   - `AI_INTERACTION_LOG.md`
   - `docs/AI_USAGE_REPORT.md`
   - All individual attempt reports.

   Ensure that Section 2.2 is properly addressed.

   Every development interaction should document:

   1. Original prompt given to AI, verbatim.
   2. AI response, verbatim.
   3. What we interpreted from it.
   4. What we planned.
   5. What we implemented.
   6. What we obtained and whether it worked.
   7. How we obtained it, including independent research, debugging and modifications.
   8. Strengths, weaknesses and trade-offs.

   Also ensure that the report compares actual development effort with the effort that would have been required without AI assistance.

   Preserve authentic records. Never fabricate prompts, AI responses, debugging experiences or test results.

   Make the development progression clear and chronological.

   ## 3. Final implementation — Section 3.2

   Review the actual source code to ensure the two specific technical requirements are genuinely implemented.

   **A. Shape class hierarchy**

   The assignment asks for a hierarchy of ExTetromino shapes, classified by:

   - Shape characteristics.
   - Bounding boxes.
   - Holes produced while landing in different orientations.

   It also asks that pieces should not simply be initialized from hardcoded matrices.

   Verify that:

   - Shapes are generated algorithmically.
   - The implementation uses an appropriate class hierarchy.
   - Bounding-box classifications are actually instantiated.
   - Orthogonal and diagonal connectivity are handled correctly.
   - Landing-hole classifications are actually instantiated.
   - Different orientations are considered when calculating landing holes.
   - The seven classic tetrominoes can be identified appropriately.

   Check that the factory actually creates objects belonging to the intended subclasses, rather than merely defining unused classes.

   **B. Functional-OO distributions**

   The assignment specifically asks to replace the original repeated-index probability approach with a functional-OO approach.

   Verify that:

   - Piece-selection distributions are implemented as proper classes.
   - Different probability distributions are supported.
   - The implementation is composable and extensible.
   - The probability of selecting pieces can be changed without modifying hardcoded piece lists.

   Ensure the actual implementation matches what the documentation claims.

   Do not add unnecessary distribution strategies or functionality beyond what is justified by the assignment and existing design.

   ## 4. Final submission requirements — Section 3

   Verify that the final project is a usable bundle of programs, source code, scripts and documentation.

   The assignment expects a game programmer to be able to create and release an ExTetris variant without requiring expertise in a programming language.

   Review the existing implementation and ensure that the following are properly provided:

   - Core ExTetris engine.
   - Extensible shape hierarchy.
   - Board and game mechanics.
   - Piece distribution configuration.
   - Appropriate application programming interface.
   - Build and run scripts or Makefile.
   - Configuration and variant creation facilities.

   Do not introduce additional systems unrelated to these objectives.

   ## 5. Documentation — Section 3.1

   Review and correct the existing:

   - `docs/DESIGN.md`
   - `docs/UML.md`
   - `docs/API.md`
   - `docs/GAME_PROGRAMMERS_MANUAL.md`
   - `docs/AI_USAGE_REPORT.md`
   - `README.md`

   Ensure that all documentation:

   - Accurately describes the final implementation.
   - Uses correct class names, relationships and method names.
   - Includes appropriate UML or graphical representations.
   - Explains the API correctly.
   - Explains how a game programmer can create and release a variant.
   - Documents AI usage and development honestly.

   The Game Programmer's Manual should be understandable to someone without programming expertise.

   Do not document features that do not exist.

   ## 6. Testing and packaging

   Test the existing implementation and fix genuine problems directly related to the assignment.

   In particular, address the previously identified issues:

   - Tkinter tests incorrectly assuming a graphical display is available.
   - Packaging tests failing because dependencies cannot be downloaded in an offline environment.
   - `setup.sh` using `--no-deps`, potentially preventing dependency installation.

   Ensure that testing reports accurately distinguish passed, failed and skipped tests.

   Verify the Makefile, installation procedure, run scripts and final ZIP.

   The final archive must contain the source, necessary scripts, documentation and preserved historical attempts.

   ## 7. Final audit

   Before completing the work, cross-check the actual implementation against the assignment PDF.

   Verify that:

   - Every assignment requirement is addressed.
   - Both Section 3.2 technical requirements are genuinely implemented.
   - All eight Section 2.2 reporting elements are covered.
   - Earlier attempts are preserved.
   - Documentation accurately reflects the code.
   - The final package is reproducible and usable.

   If anything required by the assignment is incomplete, fix it.

   If something is not required by the assignment, do not add it merely for the sake of improvement.

   ## 8. Final deliverables

   Provide:

   1. A concise summary of the deficiencies found.
   2. All changes made, with file paths.
   3. Confirmation that historical attempts were preserved.
   4. Actual test results.
   5. Any remaining limitations.
   6. Final project folder structure.
   7. A consolidated final ZIP.
   8. An honest rating out of 10 against the original assignment.

   **Final instruction:** The goal is not to build a bigger or more complicated Tetris project. The goal is to fulfil the professor's exact expectations exceptionally well, demonstrate genuine continued development, and submit a technically correct, well-documented and reproducible result.

   Stay within the assignment. Ask my permission before any proposed deviation. Do not fabricate evidence or claim completion without verification.
   ````

2. **AI Assistant's Response (Verbatim):**
   ````markdown
   [Intermediate Status Update 1 — Verbatim]
   Running the final Git tag update, submission ZIP build, full test suite, and offline packaging verification in the background (`task-776`); waiting for completion.

   [Final Assistant Response — Verbatim]
   The final review and targeted portability/testing pass against [PoPL2026AssignmentExTetris.pdf](file:///Users/vanshsharma/Documents/POPL/PoPL2026AssignmentExTetris.pdf) is complete, committed, tagged (`attempt-5-final` at `fa26c1f`), and packaged.

   ---

   ### 1. Summary of Deficiencies Found
   Four real portability and consistency issues were found during the final audit (no extra unrequested features were added):
   1. **Tkinter availability assumed a graphical display:** `TkinterRenderer.is_available()` only tested `import tkinter`, which succeeds on headless Linux/POSIX without `$DISPLAY`, and `test_optional_tk_renderer` silently returned instead of calling `self.skipTest(...)` when Tk was unavailable.
   2. **`setup.sh` hardcoded `--no-deps`:** `./setup.sh` and `./setup.sh --venv` ran `pip install --no-deps -e .`, preventing automatic installation of `numpy` into a fresh `.venv`.
   3. **Offline packaging test failure:** `test_submission_package.py` hard-failed when `pip install` inside the isolated `venv` could not reach PyPI in an offline environment, conflating lack of network access with a broken package.
   4. **CLI preset drift:** `extetris/cli.py` (`_apply_variant_preset`) had slightly different `extended` / `chaos` parameters from [configs/extended.json](file:///Users/vanshsharma/Documents/POPL/configs/extended.json) and [configs/chaos.json](file:///Users/vanshsharma/Documents/POPL/configs/chaos.json).

   ---

   ### 2. Changes Made
   - [extetris/renderers/renderers.py](file:///Users/vanshsharma/Documents/POPL/extetris/renderers/renderers.py#L283-L293): Updated `TkinterRenderer.is_available()` to instantiate and clean up a hidden `tk.Tk()` window (`withdraw()`, `update_idletasks()`, `destroy()`), returning `False` when display/Tk initialization fails.
   - [tests/test_integration/test_integration.py](file:///Users/vanshsharma/Documents/POPL/tests/test_integration/test_integration.py#L35-L47): Updated `test_optional_tk_renderer` to call `self.skipTest("Tkinter or graphical display unavailable")` when `TkinterRenderer.is_available()` is `False`, and added `test_tk_is_available_returns_false_without_display` (mocking `tk.Tk` to raise `tk.TclError`).
   - [setup.sh](file:///Users/vanshsharma/Documents/POPL/setup.sh): Removed default `--no-deps` so `./setup.sh` and `./setup.sh --venv` run `pip install -e .` (installing runtime dependencies), while keeping an explicit `--offline` flag for `--no-build-isolation --no-deps -e .`.
   - [tests/test_packaging/test_submission_package.py](file:///Users/vanshsharma/Documents/POPL/tests/test_packaging/test_submission_package.py#L52-L77): Detected offline/PyPI network errors during isolated `venv` installation and called `self.skipTest(...)` instead of misreporting them as packaging failures, while still failing on genuine build/install errors.
   - [extetris/cli.py](file:///Users/vanshsharma/Documents/POPL/extetris/cli.py#L12-L21): Synced `_apply_variant_preset()` defaults (`extended`, `chaos`, `custom`) with [configs/](file:///Users/vanshsharma/Documents/POPL/configs).
   - [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md#L1215-L1249), [docs/AI_USAGE_REPORT.md](file:///Users/vanshsharma/Documents/POPL/docs/AI_USAGE_REPORT.md#L54), and [attempts/README.md](file:///Users/vanshsharma/Documents/POPL/attempts/README.md#L17): Documented `INT-027` and updated the Attempt 5 mapping and tag `attempt-5-final` (`cfd1a1f` / `fa26c1f`).

   ---

   ### 3. Confirmation of Historical Attempt Preservation
   All earlier attempts and verbatim chronological records remain intact and unmodified in history:
   - [attempts/attempt_0_appendix_baseline/](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_0_appendix_baseline) (`attempt-0-baseline`)
   - [attempts/attempt_1_naive_oop/](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_1_naive_oop) (`attempt-1-naive-oop`)
   - [attempts/attempt_2_shape_hierarchy/](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_2_shape_hierarchy) (`attempt-2-shape-hierarchy`)
   - [attempts/attempt_3_engine_and_distributions/](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_3_engine_and_distributions) (`attempt-3-engine-and-distributions`)
   - [attempts/attempt_4_designer_and_tests/](file:///Users/vanshsharma/Documents/POPL/attempts/attempt_4_designer_and_tests) (`attempt-4-designer-and-tests`)
   - [AI_INTERACTION_LOG.md](file:///Users/vanshsharma/Documents/POPL/AI_INTERACTION_LOG.md) retains all **27** entries (`INT-001` through `INT-027`) covering all 8 Section 2.2 items cleanly with no duplicates.

   ---

   ### 4. Actual Test Results (Post-Final-Edit)
   - **Full suite (`./test.sh`, online workstation with Tk display available):**
     - **24 passed, 0 failed, 0 skipped** in **14.41s** across all 9 test suites (`test_board`, `test_configuration`, `test_distributions`, `test_engine`, `test_integration`, `test_packaging`, `test_persistence`, `test_rotations`, `test_shapes`), including live `ExTetris_Studio.ipynb` notebook execution and clean-venv packaging verification.
   - **Simulated offline packaging check (`HTTPS_PROXY=http://127.0.0.1:9 HTTP_PROXY=http://127.0.0.1:9 python3 -m pytest tests/test_packaging/test_submission_package.py -v`):**
     - **1 skipped, 0 failed, 0 passed** in **10.59s** (builds and extracts `dist/extetris_submission.zip`, creates clean `venv`, and cleanly skips when `pip install` cannot reach PyPI).

   ---

   ### 5. Remaining Limitations
   - **Offline isolated `venv` install:** In a completely air-gapped environment without internet access or pre-cached Python wheels (`numpy`, `setuptools`), `./setup.sh --offline` requires `numpy` already present in the active Python environment, and `test_submission_package.py` skips the isolated `pip install` step after verifying ZIP generation and extraction.
   - **Callable combinator persistence:** `extetris/engine/persistence.py` restores JSON-serializable distributions (`Uniform`, `Weighted`, `Bag`, `AdaptiveDifficulty`, `Markov`); arbitrary Python-callable combinators (`filter`/`map`/`blend`/`conditional`) serialize only their materialized pool (`UniformDistribution`) because Python lambdas/functions are not JSON-serializable.

   ---

   ### 6. Final Project Folder Structure (Included in Submission ZIP)
   ```text
   .
   ├── AI_INTERACTION_LOG.md
   ├── ExTetris_Studio.ipynb
   ├── LICENSE
   ├── Makefile
   ├── README.md
   ├── pyproject.toml
   ├── run.sh
   ├── setup.sh
   ├── test.sh
   ├── attempts/
   │   ├── README.md
   │   ├── attempt_0_appendix_baseline/
   │   ├── attempt_1_naive_oop/
   │   ├── attempt_2_shape_hierarchy/
   │   ├── attempt_3_engine_and_distributions/
   │   └── attempt_4_designer_and_tests/
   ├── configs/
   │   ├── chaos.json
   │   ├── classic.json
   │   ├── custom.json
   │   └── extended.json
   ├── docs/
   │   ├── AI_USAGE_REPORT.md
   │   ├── API.md
   │   ├── DESIGN.md
   │   ├── GAME_PROGRAMMERS_MANUAL.md
   │   └── UML.md
   ├── extetris/
   │   ├── __init__.py
   │   ├── builder.py
   │   ├── cli.py
   │   ├── packaging.py
   │   ├── board/
   │   ├── config/
   │   ├── distributions/
   │   ├── engine/
   │   ├── renderers/
   │   └── shapes/
   └── tests/
       ├── test_board/
       ├── test_configuration/
       ├── test_distributions/
       ├── test_engine/
       ├── test_integration/
       ├── test_packaging/
       ├── test_persistence/
       ├── test_rotations/
       └── test_shapes/
   ```

   ---

   ### 7. Consolidated Final Submission ZIP
   - **Archive:** [dist/extetris_submission.zip](file:///Users/vanshsharma/Documents/POPL/dist/extetris_submission.zip)
   - **Exact Size & Contents:** **124 files**, **229,775 bytes** (rebuilt via `make package` after the final commit). Excludes `.git/`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `dist/`, and `answers.txt` (`Has answers.txt: False`). *(Note: your earlier [dist/vansh_POPL.zip](file:///Users/vanshsharma/Documents/POPL/dist/vansh_POPL.zip) file was left untouched in `dist/`.)*

   ---

   ### 8. Honest Rating Against `PoPL2026AssignmentExTetris.pdf`
   - **Score: 9.5 / 10**
   - **Rationale:** Every core assignment mandate is genuinely and thoroughly satisfied:
     - **Section 2.2 (Highest Weight):** Complete, unvarnished chronological progression preserved across 6 Git-tagged snapshots (`attempt-0-baseline` through `attempt-5-final`), `INT-001`..`INT-027` documenting all 8 required elements, real observed bugs, and a candid effort comparison in [docs/AI_USAGE_REPORT.md](file:///Users/vanshsharma/Documents/POPL/docs/AI_USAGE_REPORT.md).
     - **Section 3.2 Technical Core:** Zero-matrix `(r, c)` shape representation synthesizing all **110** 4-polyplets with multi-axis composite subclass instantiation (`Box*`, `OrthogonalTetromino`/`DiagonalPolyplet`, `FlatLanding`/`SingleCavity`/`MultiCavity`) and first-class Functional-OO `ShapeDistribution` strategies + combinators.
     - **Sections 3 & 3.1 Usability & Docs:** Cleanly decoupled engine/renderers, no-code variant authoring via JSON + `ExTetris_Studio.ipynb` + `export_variant`, accurate technical/UML/API/designer manuals, and `24/24` passing tests.
     - **Why not 10/10:** Custom lambda-based distribution combinators degrade to `UniformDistribution` over their filtered pool on save/load due to JSON non-serializability of Python callables, and offline clean-venv packaging verification still requires either PyPI access or pre-cached wheels (`1 skipped` when offline).
   ````

3. **What I Interpreted:**
   Even when all tests pass on a networked macOS workstation with a display server, a grader running in headless Linux/WSL or an offline sandbox would hit failures if `TkinterRenderer.is_available()` ignores `$DISPLAY`, `setup.sh` skips `numpy` with `--no-deps`, or `test_submission_package.py` treats offline PyPI errors as packaging bugs.

4. **What I Planned:**
   Fix only those concrete bugs within the existing assignment scope—without altering preserved historical attempts or adding extra features—and verify both online and simulated-offline test runs.

5. **What I Implemented:**
   - [extetris/renderers/renderers.py](extetris/renderers/renderers.py): `TkinterRenderer.is_available()` now probes `tk.Tk()` and destroys it cleanly.
   - [tests/test_integration/test_integration.py](tests/test_integration/test_integration.py): `test_optional_tk_renderer` skips via `self.skipTest(...)` when display is unavailable; added `test_tk_is_available_returns_false_without_display`.
   - [setup.sh](setup.sh): removed `--no-deps` from default `pip install -e .` and added explicit `--offline` flag.
   - [tests/test_packaging/test_submission_package.py](tests/test_packaging/test_submission_package.py): added clean `self.skipTest(...)` detection on network/offline pip failures.
   - [extetris/cli.py](extetris/cli.py): synced `_apply_variant_preset` defaults with `configs/*.json`.
   - [docs/AI_USAGE_REPORT.md](docs/AI_USAGE_REPORT.md): documented `INT-027` post-audit fixes.

6. **What I Got (Did It Work?):**
   Yes—verified in both online and simulated-offline modes:
   - Simulated offline packaging test (`HTTPS_PROXY=http://127.0.0.1:9`): `1 skipped in 12.20s` (cleanly skips after building and extracting the ZIP when isolated `pip install` cannot reach PyPI).
   - Full suite (`./test.sh`): `24 passed in 18.71s` across all 9 test categories (including `test_tk_is_available_returns_false_without_display` and `test_clean_venv_install_tests_cli_and_config`).
   - Rebuilt submission ZIP (`make package`): `dist/extetris_submission.zip` (`124 files, 229658 bytes`).

7. **How I Got It (Modifications & Independent Research):**
   Confirmed via `setup.sh` inspection that `--no-deps` would leave a fresh `.venv` without `numpy`, and confirmed via `renderers.py` inspection that `import tkinter` succeeds even when `$DISPLAY` is missing on POSIX headless systems.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Accurately distinguishes `PASSED`, `FAILED`, and `SKIPPED` across headless and offline environments without masking real packaging defects.
   - **Weaknesses:** In an offline sandbox without cached wheels, `test_submission_package.py` skips the isolated venv install step after verifying ZIP creation and extraction.
