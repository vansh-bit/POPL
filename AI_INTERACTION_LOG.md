# Central AI Interaction Log

> **Assignment Requirement (Section 2.2 & Submission Instructions):**  
> This file is the single chronological source of truth for **verbatim** AI prompts, **verbatim** AI responses, interpretations, plans, implementations, test results, manual modifications/research, and trade-offs across every attempt—including earlier failed or less-successful attempts.  
> Individual `ATTEMPT_N_REPORT.md` files and `docs/AI_USAGE_REPORT.md` reference entries here by Interaction ID (`INT-001`, `INT-002`, ...).

## Metadata
- **Assistant / Tool Used:** Antigravity (Gemini 4 Hydrogen High)
- **Project:** Extended Tetris (ExTetris) — CS F301 PoPL

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

---

## INT-001 — [Attempt 0] Reproduce Appendix A–D Baseline & Run Diagnostic Probes
- **Timestamp:** 2026-11-26 02:18 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   start attempt 0 only
   ```

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Transcribed Appendices A–D from `PoPL2026AssignmentExTetris.pdf` verbatim into `attempts/attempt_0_appendix_baseline/` (`engine.py`, `board.py`, `shape.py`, `allextetrominoes.py`) without modifying or fixing bugs, and executed non-interactive Python diagnostic probes against them.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Copied the 4 Attempt 0 files into `attempts/attempt_1_naive_oop/` and applied only the 5 targeted bug fixes across `engine.py`, `board.py`, `shape.py`, and `allextetrominoes.py`, then ran AST/import/boundary/mutation verification checks.

   Observed verification output:
   ```text
   1. Explicit imports & zero eval() calls verified.
   2. pauseStatus typo & game_over_status handling verified.
   3. Shape.__init__ defensive copy & non-mutable default verified.
   4. Board.collision negative offsets & boundaries verified.
   5. Out-of-range lookup safely raised ValueError: Extetromino index out of range: 99 (expected 1..73)
        887
   ```

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Refactored `shape.py`, `allextetrominoes.py`, and `engine.py` inside `attempts/attempt_1_naive_oop/` to introduce `ClassicTetromino` and `ExtendedTetromino` subclasses of `Shape`, replace the 73 module-level globals with a deduplicated `PieceRegistry` (71 unique matrices), and preserve subclass identity across rotations via `Shape.clone()`.

   Observed verification output:
   ```text
   1. Zero Extetromino* globals verified.
   2. 71 unique matrices verified (duplicates [1, 10, 11] removed).
   3. Exact parity with Attempt 0 deduplicated catalog verified.
   4. Subclasses (7 Classic, 64 Extended), clone(), and 4-rotation invariance verified for all 71 pieces.
        934
   ```

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Updated `attempts/attempt_1_naive_oop/engine.py` to move timer scheduling (`window.after(...)`) and `window.mainloop()` out of `__init__` into `run()`, added `headless=False` mode (guarding Tkinter widgets/dialogs when `headless=True`), and executed 5 headless gameplay smoke tests.

   Observed output:
   ```text
   SMOKE 1 PASS: Movement & wall boundaries OK, rightmost cursor = (0, 6)
   SMOKE 2 PASS: CW/CCW rotation, subclass preservation & collision rejection OK
   SMOKE 3 PASS: Pause/resume input gating OK
   SMOKE 4 PASS: Line clearing OK, deleted_lines = 1
   SMOKE 5 PASS: Game-over detection & new_game() reset OK
   ```

3. **What I Interpreted:**
   Because `TetrisEngine.__init__` originally started `window.mainloop()`, the engine could not be tested programmatically or run without a GUI window. Separating construction from `run()` and supporting `headless=True` lets us verify core gameplay mechanics cleanly.

4. **What I Planned:**
   Move Tkinter `after()` timers and `mainloop()` into `TetrisEngine.run()`, guard Tk widget references when `headless=True`, keep `if __name__ == "__main__":` calling `tetris_engine.run()`, and write inline smoke assertions covering walls, rotations, pause gating, line clearing, and game over/reset.

5. **What I Implemented:**
   - [attempts/attempt_1_naive_oop/engine.py](attempts/attempt_1_naive_oop/engine.py): added `headless=False` parameter to `TetrisEngine.__init__`, extracted `TetrisEngine.run()`, added `game_over_status` guards in input handlers, added bounds check in `render()`, and updated `__main__` to call `tetris_engine.run()`.

6. **What I Got (Did It Work?):**
   Yes—`py_compile` succeeded and all 5 headless smoke tests (`Movement`, `CW/CCW Rotation`, `Pause/Resume`, `Line Clearing`, `Game Over & Reset`) passed cleanly with exit code `0`.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Executed an exhaustive combinatorial audit of all 8-connected 4-polyplets on a `4×4` grid and compared them against Attempt 1's 71 deduplicated matrices in `attempts/attempt_1_naive_oop/allextetrominoes.py`, alongside a structural review against PDF Section 3.2 and the target design specification.

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

3. **What I Interpreted:**
   This audit establishes the exact mathematical and architectural evidence showing why Attempt 1's matrix-wrapped OOP approach is insufficient and why Attempt 2 and Attempt 3 are necessary.

4. **What I Planned:**
   Compute the exact count of fixed (110), one-sided (34), and free (22) 8-connected 4-polyplets on a `4×4` grid, compare them with Attempt 1's 71 matrices, inspect bounding boxes, and evaluate Section 3.2 / target-architecture gaps.

5. **What I Implemented:**
   Ran a non-destructive Python combinatorial audit script over `attempts/attempt_1_naive_oop/allextetrominoes.py`. (No code edits in this step.)

6. **What I Got (Did It Work?):**
   Yes—the audit revealed that Attempt 1 covers 71 of 110 fixed orientations (missing 39) while containing 21 redundant rotation-equivalent groups across the 34 one-sided polyplets, and confirmed 5 shapes each in `(3, 4)` and `(4, 3)` bounding boxes.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Created `attempts/attempt_1_naive_oop/ATTEMPT_1_REPORT.md`, logged `INT-006` in `AI_INTERACTION_LOG.md`, committed Attempt 1 to Git, tagged the snapshot `attempt-1-naive-oop`, and updated `attempts/README.md` with the recorded commit hash.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `attempts/attempt_2_shape_hierarchy/shape.py` with coordinate-only `Shape` and `ExTetromino` classes (`normalize_coords`, `is_connected`, `rotateCW`, `rotateAntiCW`, `fliplr`, `flipud`, `bounding_box`, `to_matrix`, `landing_holes`, `landing_hole_profile`, `is_orthogonal`, `is_diagonal`) and verified against `numpy.rot90` / `fliplr` / `flipud` plus invalid-piece checks.

   Observed output:
   ```text
   1. Normalization anchored at (0, 0) verified: ((0, 0), (0, 1), (1, 1), (2, 2))
   2. CW, AntiCW, 4xCW, fliplr, flipud, bounding_box, and to_matrix verified.
   3. Landing holes & 4-rotation profiles verified: {'I': (0, 0, 0, 0), 'O': (0, 0, 0, 0), 'T': (2, 1, 0, 1), 'Diamond': (3, 3, 3, 3)}
   4. Rejected invalid piece as expected: ExTetromino must have exactly 4 cells, got 3.
   4. Rejected invalid piece as expected: ExTetromino cells must be 8-connected, got ((0, 0), (0, 2), (0, 3), (0, 4)).
   ```

3. **What I Interpreted:**
   Eliminating stored matrices in favor of normalized `(r, c)` coordinate tuples satisfies PDF Section 3.2 and makes geometric queries (bounding box, rotation, connectivity, and landing cavities) direct and exact.

4. **What I Planned:**
   Create `Shape` (normalized `(r, c)` representation, affine grid rotations/reflections, on-demand `to_matrix()`, and `landing_holes()` / `landing_hole_profile()`) and `ExTetromino(Shape)` (enforcing 4 cells + 8-connectivity and providing 4-connectivity vs. diagonal morphology checks).

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/shape.py](attempts/attempt_2_shape_hierarchy/shape.py): `normalize_coords()`, `is_connected()`, `Shape`, and `ExTetromino`.

6. **What I Got (Did It Work?):**
   Yes—normalization from negative/shifted offsets, rotation/reflection parity against NumPy (`np.rot90`, `np.fliplr`, `np.flipud`), landing-hole profiles across 4 rotations, and validation rejections for invalid cell counts and disconnected pieces all passed with exit code `0`.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `ExTetrominoFactory` in `attempts/attempt_2_shape_hierarchy/factory.py` using exhaustive 4-cell combinations on a `4×4` grid filtered by 8-connectivity and normalized to `(0, 0)`, exposing `all_fixed()`, `all_one_sided()`, `all_free()`, `classic_one_sided()`, `classic_fixed()`, `extended_one_sided()`, `extended_fixed()`, `by_id()`, `filter()`, and `summary()`.

   Observed output:
   ```text
   ExTetrominoFactory summary: {'fixed_total': 110, 'one_sided_total': 34, 'free_total': 22, 'classic_one_sided': 7, 'classic_fixed': 19, 'diagonal_one_sided': 27, 'diagonal_fixed': 91, 'generation_time_sec': 0.011993}
   1. All combinatorial counts verified: 110 fixed, 34 one-sided, 22 free, 7/19 classic, 27/91 diagonal.
   2. Zero duplicate IDs and zero duplicate coordinate sets verified.
   3. 8-connectivity and (0, 0) normalization verified on all 110 shapes.
   4. Clone isolation and by_id() verified.
   ```

3. **What I Interpreted:**
   Rather than storing or fixing the 71 starter matrices from Attempt 1, generating all 4-polyplets combinatorially from `(r, c)` coordinates guarantees completeness (110 fixed, 34 one-sided, 22 free) and lets us separate classic 4-connected tetrominoes (7 one-sided / 19 fixed) cleanly from diagonal polyplets (27 / 91).

4. **What I Planned:**
   Enumerate `C(16, 4)` subsets on a `4×4` grid, filter via `is_connected(..., diagonal=True)`, normalize via `normalize_coords()`, order deterministically into IDs `1..110`, return clones from all query methods, and include an `_instantiate_piece()` hook for Prompt 3's subclass hierarchy.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/factory.py](attempts/attempt_2_shape_hierarchy/factory.py): `ExTetrominoFactory` with `all_fixed`, `all_one_sided`, `all_free`, `classic_one_sided`, `classic_fixed`, `extended_one_sided`, `extended_fixed`, `by_id`, `filter`, and `summary`.

6. **What I Got (Did It Work?):**
   Yes—all 110 fixed, 34 one-sided, 22 free, 7 classic one-sided, 19 classic fixed, 27 diagonal one-sided, and 91 diagonal fixed counts, normalization invariants, 8-connectivity, unique IDs `1..110`, and clone isolation passed in `0.011993` seconds.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `attempts/attempt_2_shape_hierarchy/hierarchy.py` with cooperative multiple-inheritance subclasses across all three classification axes and updated `ExTetrominoFactory._instantiate_piece()` in `factory.py` to synthesize and instantiate the matching composite subclass for each of the 110 pieces.

   Observed output:
   ```text
   1. All 110 pieces verified across all 3 classification axes:
      Bounding boxes: [('Box1x4Shape', 1), ('Box2x2Shape', 1), ('Box2x3Shape', 12), ('Box2x4Shape', 14), ('Box3x2Shape', 12), ('Box3x3Shape', 33), ('Box3x4Shape', 10), ('Box4x1Shape', 1), ('Box4x2Shape', 14), ('Box4x3Shape', 10), ('Box4x4Shape', 2)]
      Morphology: {'OrthogonalTetromino': 19, 'DiagonalPolyplet': 91}
      Cavities: {'FlatLandingShape': 8, 'MultiCavityShape': 81, 'SingleCavityShape': 21}
   2. Dynamic reclassification on rotation verified: Box1x4Shape -> Box4x1Shape.
   3. Invariant check rejected mismatched subclass: Box3x4Shape requires bounding box (3, 4), got (2, 2)
   ```

3. **What I Interpreted:**
   To avoid an explosion of 66 hand-written classes (`11 boxes × 2 morphologies × 3 cavities`), we can define the 3 clean axis hierarchies with invariant checks and combine them via cooperative MRO + cached composite subclasses, wired into `ExTetrominoFactory`.

4. **What I Planned:**
   Create `Box1x4Shape`..`Box4x4Shape` (explicitly including `Box3x4Shape`, `Box4x3Shape`, `Box4x1Shape`), `OrthogonalTetromino`/`DiagonalPolyplet`, `FlatLandingShape`/`SingleCavityShape`/`MultiCavityShape`, plus `classify_extetromino()`, and hook `ExTetrominoFactory._instantiate_piece()` to use it.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/hierarchy.py](attempts/attempt_2_shape_hierarchy/hierarchy.py): all 11 bounding-box classes, 2 morphology classes, 3 landing-cavity classes, `get_composite_class()`, and `classify_extetromino()`.
   - [attempts/attempt_2_shape_hierarchy/factory.py](attempts/attempt_2_shape_hierarchy/factory.py): hooked `_instantiate_piece()` to `classify_extetromino()`.

6. **What I Got (Did It Work?):**
   Yes—all 110 generated shapes classified cleanly across all 11 bounding boxes (`10` each in `Box3x4Shape` and `Box4x3Shape`), both morphologies (`19` orthogonal, `91` diagonal), and all 3 cavity categories (`8` flat, `21` single, `81` multi), with dynamic reclassification on rotation and invariant rejection on mismatched construction.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented coordinate-aware `Board` (`board.py`), updated `TetrisEngine` (`engine.py`) to draw from `ExTetrominoFactory` and reclassify pieces on rotation, and added `test_attempt2.py` covering shape generation, hierarchy, rotations, board boundaries, line clearing, headless gameplay, and Tkinter initialization.

   Initial run failed 1 of 8 tests (`test_engine_headless_gameplay_and_gameover` in `0.803s`) because setting `board.area[0:2, :] = True` filled entire rows, which `clear_full_lines()` immediately cleared. Updating the test fixture to occupy only spawn columns `board.area[1:4, 3:8] = True` fixed the test, yielding:
   ```text
   Ran 8 tests in 0.298s

   OK
   ```

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Audited line counts, imports (`tkinter` isolated to `engine.py` and GUI smoke test; zero `eval()` across all 6 files), and remaining architectural gaps; wrote `attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md`; logged `INT-011` in `AI_INTERACTION_LOG.md`; committed and tagged `attempt-2-shape-hierarchy`; and updated `attempts/README.md`.

   Observed audit output:
   ```text
   board.py: lines=99, imports_tkinter=False, has_eval=False
   engine.py: lines=266, imports_tkinter=True, has_eval=False
   factory.py: lines=138, imports_tkinter=False, has_eval=False
   hierarchy.py: lines=181, imports_tkinter=False, has_eval=False
   shape.py: lines=221, imports_tkinter=False, has_eval=False
   test_attempt2.py: lines=162, imports_tkinter=True, has_eval=False
   ```

3. **What I Interpreted:**
   With the shape hierarchy and 110-polyplet factory verified, we need an explicit audit of what Attempt 2 resolved vs. what engine, distribution, renderer, and heuristic gaps motivate Attempt 3 before freezing the Attempt 2 snapshot.

4. **What I Planned:**
   Audit Attempt 2 modules for coupling and missing features, capture the synthesis in `ATTEMPT_2_REPORT.md`, commit and tag `attempt-2-shape-hierarchy`, and update `attempts/README.md`.

5. **What I Implemented:**
   - [attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md](attempts/attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md).

6. **What I Got (Did It Work?):**
   Yes—all 6 files audited cleanly, `ATTEMPT_2_REPORT.md` finalized, and the Attempt 2 snapshot is committed and tagged `attempt-2-shape-hierarchy`.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Bootstrapped `attempts/attempt_3_engine_and_distributions/` with Attempt 2's coordinate shape modules (`shape.py`, `hierarchy.py`, `factory.py`), implemented upgraded `Board` heuristics (`board.py`) and the Functional-OO `ShapeDistribution` hierarchy + combinators (`distributions.py`), and verified everything with seeded tests (`test_board_and_distributions.py`).

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `ExTetrisEngine` and `GameState` in `attempts/attempt_3_engine_and_distributions/engine.py` with zero UI imports, and ran verification checks on FSM transitions, Observer events, wall kicks, ghost projection, soft/hard drop scoring, and level/speed scaling.

   Observed output:
   ```text
   1. Zero tkinter/UI dependency in engine.py verified.
   2. 4-state FSM READY -> RUNNING -> PAUSED -> RUNNING verified.
   3. Wall-kick (0, -2) rotation recovery verified at right wall.
   4. Ghost projection, composite matrix, soft drop (+1) & hard drop (+2/cell) verified.
   5. Level/speed progression (12 lines -> level 2, 920ms) & Observer events verified.
   6. GAME_OVER transition & Observer event verified.
   ```

3. **What I Interpreted:**
   To completely decouple game rules from presentation, `ExTetrisEngine` must own the 4-state FSM, piece spawning, wall kicks, ghost projection, scoring, and speed progression without importing any UI toolkit, communicating outward strictly through `register_callback()` events and `get_render_composite()`.

4. **What I Planned:**
   Define `GameState` enum (`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`), implement `ExTetrisEngine` lifecycle methods (`start`, `pause`, `resume`, `toggle_pause`, `new_game`), wall-kick offsets `((0, 0), (0, -1), (0, 1), (0, -2), (0, 2))`, soft/hard drop scoring (`+1`/`+2`), level/speed progression, `get_render_composite()`, and Observer dispatch (`*` + named events).

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/engine.py](attempts/attempt_3_engine_and_distributions/engine.py): `GameState` and `ExTetrisEngine`.

6. **What I Got (Did It Work?):**
   Yes—`py_compile` and all 6 verification assertions passed with exit code `0`, confirming zero `tkinter` imports, exact FSM transitions, `(0, -2)` wall-kick recovery, `+1`/`+2` drop scoring, level `2` (`920 ms`) after 12 lines cleared, and `GAME_OVER` Observer events.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `AbstractRenderer`, `HeadlessRenderer`, `NonBlockingKeyReader`, `CLIRenderer`, optional `TkinterRenderer`, and `create_renderer()` in `attempts/attempt_3_engine_and_distributions/renderers.py`, plus `play.py` CLI runner supporting `--renderer headless|cli|tk`.

   Observed verification output (`play.py --renderer headless --variant extended --seed 42 --steps 25` + renderer checks):
   ```text
   Captured 26 headless frames. Final score=0, state=RUNNING
   1. HeadlessRenderer scripted simulation verified, frames captured: 6
   2. CLIRenderer ANSI output, key controls, and non-TTY run verified.
   3a. TkinterRenderer.is_available(): True
   3b. Optional TkinterRenderer render & close verified.
   3c. Graceful degradation verified when Tk absent: Tkinter is not available in this Python environment.
   ```

3. **What I Interpreted:**
   To prove the engine is truly decoupled from UI toolkits, all rendering and input must live behind `AbstractRenderer`, with `HeadlessRenderer` and `CLIRenderer` as first-class targets and `TkinterRenderer` imported lazily so headless/no-display environments never crash.

4. **What I Planned:**
   Create `AbstractRenderer` with `attach/render/run/close`, `HeadlessRenderer` with frame/composite/snapshot capture and scripted actions, `CLIRenderer` with `termios`/`select` + `msvcrt` non-blocking key polling and ANSI frame formatting, lazy `TkinterRenderer` with `is_available()`, and `play.py` CLI runner.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/renderers.py](attempts/attempt_3_engine_and_distributions/renderers.py)
   - [attempts/attempt_3_engine_and_distributions/play.py](attempts/attempt_3_engine_and_distributions/play.py)

6. **What I Got (Did It Work?):**
   Yes—`play.py --renderer headless` captured 26 frames showing active, ghost, and locked extended pieces; `CLIRenderer` rendered ANSI frames and processed key controls in non-TTY streams; and `TkinterRenderer` both ran when Tk was available and raised a clean `RuntimeError` when Tk was mocked absent.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Created `attempts/attempt_3_engine_and_distributions/test_attempt3.py` and executed `py_compile`, `test_attempt3.py`, and `test_board_and_distributions.py`.

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

3. **What I Interpreted:**
   Attempt 3 needs an end-to-end test suite exercising the interactions between `Board`, `ShapeDistribution` combinators, `ExTetrisEngine`, `HeadlessRenderer`, `CLIRenderer`, `TkinterRenderer` fallback, and `play.main()` together.

4. **What I Planned:**
   Write `test_attempt3.py` covering all 4 subsystem areas (board heuristics/bounds, seeded distributions & composed combinators, FSM/wall-kicks/scoring/level-floor/observers, and renderers + CLI), then run both test modules together.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/test_attempt3.py](attempts/attempt_3_engine_and_distributions/test_attempt3.py)

6. **What I Got (Did It Work?):**
   Yes—all 8 tests in `test_attempt3.py` (`2.009s`) and all 7 tests in `test_board_and_distributions.py` (`1.440s`) passed with exit code `0`.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Audited module line counts and Tkinter coupling across all 10 Python files in `attempts/attempt_3_engine_and_distributions/` (`2,278` total lines, `tkinter` absent from all core modules), wrote `ATTEMPT_3_REPORT.md`, logged `INT-016` in `AI_INTERACTION_LOG.md`, committed and tagged `attempt-3-engine-and-distributions`, and updated `attempts/README.md`.

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

3. **What I Interpreted:**
   With the decoupled engine, Functional-OO distributions, and multi-renderer layer verified (`15/15` tests), we need to document the boundary audit and remaining no-code designer gaps before freezing Attempt 3.

4. **What I Planned:**
   Inspect module coupling/line counts, write `ATTEMPT_3_REPORT.md` detailing achievements (`INT-012`..`INT-015`) and Attempt 4 gaps, commit and tag `attempt-3-engine-and-distributions`, and update `attempts/README.md`.

5. **What I Implemented:**
   - [attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md](attempts/attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md)
   - Updated [AI_INTERACTION_LOG.md](AI_INTERACTION_LOG.md) and [attempts/README.md](attempts/README.md).

6. **What I Got (Did It Work?):**
   Yes—audit confirmed clean UI isolation (`tkinter` confined to `renderers.py` and its test), `ATTEMPT_3_REPORT.md` finalized, and Attempt 3 tagged in Git.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Bootstrapped `attempts/attempt_4_designer_and_tests/` with Attempt 3's core modules, implemented `config/schema.json`, `config/validator.py` (`ConfigValidationError`, `validate_config`), and `config/loader.py` (`load_config`, `save_config`, `get_default_config`), added the 4 JSON presets under `configs/`, and tested valid loading plus 14 invalid/malformed config cases.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `ExTetrisBuilder` and `load_game_from_json()` in `builder.py`, JSON state persistence (`save_engine_state`, `load_engine_state`, `export_text_board`) in `persistence.py`, and `save_state`/`load_state`/`export_text_board` hooks on `ExTetrisEngine`.

   During initial verification, save/load/resume parity failed on the 4th move after resume (`orig: 97 26 (0, 3) rest: 97 29 (0, 3)`) because passing the deserialized `BagDistribution` into `ExTetrisEngine.__init__()` caused `_init_pieces()` to pop 2 items off `_bag` before `load_engine_state()` restored `current_piece` and `next_piece`. Assigning `engine.distribution` after `ExTetrisEngine.__init__()` resolved the bug, yielding:
   ```text
   1. Fluent ExTetrisBuilder chaining + headless run verified, score = 38
   2. load_game_from_json(configs/custom.json) verified.
   3. Empty filtered pool rejected: - Current variant and filters leave 0 matching ExTetromino shapes.
   4. export_variant() generated config/docs/launcher and ran standalone cleanly, piece_count = 9
   5. Save / Load / Resume bit-identical state & RNG continuation verified!
   6. Corrupt save file rejected: Invalid or unsupported ExTetris state file format.
   ```

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Created `attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb` wired directly to `config.load_config`/`validate_config` and `ExTetrisBuilder`, executed all 6 code cells non-interactively with `jupyter nbconvert --to notebook --execute --inplace ExTetris_Studio.ipynb`, and added `play.py` supporting `--config` JSON launching.

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

3. **What I Interpreted:**
   PDF Section 3 explicitly draws an analogy to Jupyter notebooks empowering non-programmers. `ExTetris_Studio.ipynb` must act as a true no-code studio backed 100% by `config/` and `ExTetrisBuilder` without duplicating any game rules.

4. **What I Planned:**
   Author a 6-code-cell notebook covering catalog inspection, `ipywidgets` variant controls + live validation, invalid-config rejection demo, distribution sampling preview, standalone variant export + subprocess run, and headless simulation; verify non-interactive execution via `nbconvert`; and add `play.py --config`.

5. **What I Implemented:**
   - [attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb](attempts/attempt_4_designer_and_tests/ExTetris_Studio.ipynb)
   - [attempts/attempt_4_designer_and_tests/play.py](attempts/attempt_4_designer_and_tests/play.py)

6. **What I Got (Did It Work?):**
   Yes—`jupyter nbconvert --execute` ran all 6 code cells (`exec_count=1..6`) with zero cell errors and populated outputs (`51,091` bytes), and `play.py --config configs/custom.json` launches configured variants directly.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Created 8 categorized test modules under `attempts/attempt_4_designer_and_tests/tests/` (`test_shapes`, `test_board`, `test_rotations`, `test_distributions`, `test_engine`, `test_configuration`, `test_persistence`, `test_integration`) and ran `python3 -m unittest discover -s tests -t . -v`.

   Initial run failed 1 of 22 tests (`test_wall_kicks_and_invalid_rotations` in `8.016s`) because the obstacle row was placed at row `10` instead of row `8`, leaving row `8` clear for the rotated `1×4` horizontal I-piece. Moving the obstacle row to row `8` fixed the test, yielding:
   ```text
   Ran 22 tests in 6.638s

   OK
   ```

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Audited the full file inventory under `attempts/attempt_4_designer_and_tests/` (`4,924` lines across modules, JSON schemas/presets, `ExTetris_Studio.ipynb`, and 8 categorized test suites), wrote `ATTEMPT_4_REPORT.md`, logged `INT-021` in `AI_INTERACTION_LOG.md`, committed and tagged `attempt-4-designer-and-tests`, and updated `attempts/README.md`.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Promoted Attempt 4 into the modular root `extetris/` package (`shapes/`, `board/`, `distributions/`, `engine/`, `renderers/`, `config/`, `builder.py`, `cli.py`), populated root `configs/*.json`, created and executed root `ExTetris_Studio.ipynb`, installed editable package via `pip`, and verified both `extetris` entrypoint and `python3 -m extetris.cli`.

   Observed verification output:
   ```text
   [NbConvertApp] Writing 50770 bytes to ExTetris_Studio.ipynb
   Successfully built extetris
   Installing collected packages: extetris
   Successfully installed extetris-0.1.0
   extetris --config configs/custom.json --steps 8 -> Captured 9 headless frames. Final score=0, state=RUNNING
   python3 -m extetris.cli --variant extended --renderer headless --seed 42 --steps 8 -> Captured 9 headless frames. Final score=0, state=RUNNING
   ```

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

7. **How I Got It (Modifications & Independent Research):**
   Updated `ExTetrisBuilder.export_variant()` so the generated `run_variant.py` tries `from extetris import load_game_from_json` first (for clean venv installs) and falls back to adding `REPO_ROOT` to `sys.path` when launched uninstalled from a source checkout.

8. **Strengths, Weaknesses & Trade-offs:**
   - **Strengths:** Clean installable Python package layout, console entrypoint, single source of truth across CLI, Builder, and Notebook.
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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Created `Makefile`, `setup.sh`, `run.sh`, `test.sh`, `extetris/packaging.py`, and promoted all 8 categorized test modules to root `tests/` importing directly from `extetris`.

   During initial `make package`, an inline `python3 -c` snippet with `\` line continuations raised `SyntaxError` because Make collapses continued lines onto one line. Extracted the packager cleanly into `extetris/packaging.py` (`python3 -m extetris.packaging`), after which verification passed:
   ```text
   ./test.sh -> 22 passed in 8.64s
   make package -> Created .../dist/extetris_submission.zip (123 files, 207402 bytes)
   ZIP entries count: 123
   All required entries verified and all excluded paths absent.
   ./run.sh --config configs/custom.json --steps 5 -> Captured 6 headless frames. Final score=0, state=RUNNING
   ```

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Implemented `tests/test_packaging/test_submission_package.py` covering all 6 clean-environment release verification steps and executed `./test.sh` (`pytest tests -v`).

   Observed output:
   ```text
   tests/test_packaging/test_submission_package.py::TestSubmissionPackage::test_clean_venv_install_tests_cli_and_config PASSED [ 65%]
   ...
   ============================= 23 passed in 38.86s ==============================
   ```

3. **What I Interpreted:**
   To prove the packaged ZIP works independently of our local development setup (not just via editable installs or `PYTHONPATH`), we must test building the ZIP, extracting it, installing into a fresh `python3 -m venv` with `PYTHONPATH` stripped, running the tests, invoking the installed `extetris` binary, and validating JSON configs from outside the extracted tree.

4. **What I Planned:**
   Write `TestSubmissionPackage.test_clean_venv_install_tests_cli_and_config` guarding against recursion via `EXTETRIS_SKIP_PACKAGING_TEST=1`, stripping `PYTHONPATH`/`PYTHONHOME`/`VIRTUAL_ENV`, running `pip install`, `unittest discover`, `extetris --config configs/custom.json --steps 6`, and `extetris.load_config(...)` asserting `extetris.__file__` resolves inside the temp venv.

5. **What I Implemented:**
   - [tests/test_packaging/test_submission_package.py](tests/test_packaging/test_submission_package.py)

6. **What I Got (Did It Work?):**
   Yes—all **23 tests passed in `38.86s`** on the first run (`./test.sh`), proving the packaged submission installs and runs cleanly in an isolated virtual environment.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Authored `docs/DESIGN.md`, `docs/UML.md`, `docs/API.md`, `docs/GAME_PROGRAMMERS_MANUAL.md`, and updated root `README.md` strictly matching the verified `extetris/` codebase, and verified the documented `./run.sh --config configs/custom.json --export ...` workflow end-to-end.

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

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Authored `docs/AI_USAGE_REPORT.md` synthesizing Attempts 0–5 with exact `INT-001`..`INT-026` references and effort comparison, rebuilt `dist/extetris_submission.zip`, ran `./test.sh` (all 23 tests including `tests/test_packaging/`), updated `attempts/README.md`, committed Attempt 5, and tagged `attempt-5-final`.

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
