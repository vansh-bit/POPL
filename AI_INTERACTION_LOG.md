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
