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
