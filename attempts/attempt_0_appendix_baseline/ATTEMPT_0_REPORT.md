# Attempt 0 — Appendix A–D Exact Baseline Report

- **Status:** Completed (Baseline Preserved)
- **Directory:** `attempts/attempt_0_appendix_baseline/`
- **Related Interaction IDs:** `INT-001` (see [../../AI_INTERACTION_LOG.md](../../AI_INTERACTION_LOG.md))

---

## 1. Objective
Faithfully reproduce the starter code provided in **Appendices A–D** of `PoPL2026AssignmentExTetris.pdf` (`engine.py`, `board.py`, `shape.py`, `allextetrominoes.py`) without fixing its bugs, execute diagnostic checks, and establish a concrete baseline to compare against all subsequent attempts.

## 2. Files Reproduced
| File | Appendix | Lines | Role |
|------|----------|-------|------|
| `engine.py` | Appendix A | 253 | Monolithic Tkinter UI + game loop + keyboard/menu callbacks |
| `board.py` | Appendix B | 97 | 2D NumPy boolean grid, `insertShape`, `removeShape`, `collision` |
| `shape.py` | Appendix C | 69 | Matrix wrapper with `fliplr`, `flipud`, `transpose`, `rotateCW`, `rotateAntiCW` |
| `allextetrominoes.py` | Appendix D | 116 | 73 hard-coded NumPy boolean matrices (`Extetromino1`..`Extetromino73`) + `eval`-based sampling |

*(Transcription note: PDF page screenshots on pages 5–16 were inspected directly so OCR whitespace and smart quotes were not copied into Python source.)*

## 3. Verification & Diagnostic Probes Run
Non-interactive Python probes were executed inside `attempts/attempt_0_appendix_baseline/`:

1. **Module & `shape.py` Execution:**
   - `python3 shape.py | wc -l` exited cleanly (`0`) and printed **887 lines** of rotated shapes.
2. **Audit of `allextetrominoes.py`:**
   - Defined matrices: **73** (`Extetromino1`..`Extetromino73`).
   - Unique `(shape, bytes)` pairs: **71** (duplicate group: `[1, 10, 11]`, repeating the `1×4` I-piece three times as a crude frequency boost).
   - `get_extetromino_at(99)` raised `NameError: name 'Extetromino99' is not defined` due to `eval("Extetromino"+str(index))`.
3. **Aliasing / Mutation in `Shape`:**
   - `s = Shape(allextetrominoes.Extetromino3); s.fliplr()` mutated `allextetrominoes.Extetromino3` **in-place** (`Extetromino3 mutated in place by Shape.fliplr?: True`) because `Shape.__init__` stores `self.matrix = mat` without copying.
4. **Boundary Bug in `Board.collision`:**
   - On an empty `10×20` `Board`:
     - `b.collision(Extetromino1, (0, -1))` returned **`False`** (should be `True`).
     - `b.collision(Extetromino1, (-1, 0))` returned **`False`** (should be `True`).
   - **Root cause:** `collision()` relies on catching `IndexError`, but Python/NumPy accepts negative indices (`self.area[-1]`, `self.area[0][-1]`) and silently wraps around to the opposite side of the board.
5. **Hidden Namespace Leakage & Traps in `engine.py`:**
   - `engine.py` never writes `import numpy`, yet calls `numpy.floor`, `numpy.ceil`, and `numpy.full_like`. It survives solely because `from allextetrominoes import *` leaks `numpy` into `engine`'s module globals.
   - `hasattr(tk, 'simpledialog')` is `False` right after `import tkinter as tk`, and only becomes `True` as an accidental side effect of `from tkinter import filedialog`.
   - Line 184 in `extetricks_help()` contains a typo: `self.pasueStatus = False` instead of `self.pauseStatus = False`, leaving the game permanently paused after opening *About*.
   - Line 149 (`Game Over!`) and Line 183 (`About`) instantiate `tk.simpledialog.Dialog(...)`, which opens a blocking modal window (confirmed during diagnostic run when `Dialog(None, ...)` blocked execution).

## 4. Architectural Limitations Identified (Driving Attempt 1 & Attempt 2)
1. **No `ExTetromino` Class Hierarchy:** Pieces are raw hard-coded matrices (`allextetrominoes.py`) rather than subclasses of `Shape` parameterized by bounding box, morphology, or landing cavities.
2. **Crude Distribution Mechanism:** Increasing piece probability requires repeating indices in a sequence passed to `get_any_extetromino`.
3. **Unsafe & Coupled Game Loop:** `TetrisEngine.__init__` invokes `self.window.mainloop()` directly at the end of construction, preventing headless testing, alternative renderers (CLI/Jupyter), or programmatic API control.
4. **Incomplete State Persistence:** `save_file()` only writes the rendered `tk.Text` string rather than serializable game state.
5. **Minor Gameplay/UI Bugs:** `self.pasueStatus` typo, `eval(int(input(...)))` in `__main__`, `speed_up()` only triggering at `deleted_lines % 100 == 0`, and `game_over_status` never being set to `True` on game over.
