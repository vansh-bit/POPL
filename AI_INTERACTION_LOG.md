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
| `INT-005` | Attempt 1 | Audit Attempt 1 against PDF Section 3.2 & `answers.txt` | Quantified 71 vs 110 polyplets, 21 rotation-dup groups, and 4 structural gaps |
| `INT-006` | Attempt 1 | Write `ATTEMPT_1_REPORT.md`, commit & tag `attempt-1-naive-oop` | Report written, logged, committed, and tagged |

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

## INT-005 — [Attempt 1] Audit Against PDF Section 3.2 & `answers.txt`
- **Timestamp:** 2026-11-26 10:52 IST
- **Tool / Model:** Antigravity — Gemini 4 Hydrogen (High)

1. **Prompt Given (Verbatim):**
   ```text
   Audit attempts/attempt_1_naive_oop/ against the requirements in PoPL2026AssignmentExTetris.pdf (Section 3.2) and answers.txt. Specifically check: (1) how many unique 4-polyplets are actually covered vs. missing, (2) why wrapping hard-coded matrices still violates the no-matrix-initialization requirement and lacks bounding-box/morphology/cavity classification, (3) why list-based probability distribution is still crude, and (4) why Tkinter coupling still limits extensibility
   ```

2. **AI Assistant's Response (Verbatim Execution Summary & Observed Output):**
   Executed an exhaustive combinatorial audit of all 8-connected 4-polyplets on a `4×4` grid and compared them against Attempt 1's 71 deduplicated matrices in `attempts/attempt_1_naive_oop/allextetrominoes.py`, alongside a structural review against PDF Section 3.2 and `answers.txt`.

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
   Compute the exact count of fixed (110), one-sided (34), and free (22) 8-connected 4-polyplets on a `4×4` grid, compare them with Attempt 1's 71 matrices, inspect bounding boxes, and evaluate Section 3.2 / `answers.txt` gaps.

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
