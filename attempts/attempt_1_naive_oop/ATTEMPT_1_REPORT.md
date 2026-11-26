# Attempt 1 — Naive OOP Refactor Report

- **Status:** Completed (Preserved Snapshot)
- **Directory:** `attempts/attempt_1_naive_oop/`
- **Related Interaction IDs:** `INT-002`, `INT-003`, `INT-004`, `INT-005`, `INT-006` (see [../../AI_INTERACTION_LOG.md](../../AI_INTERACTION_LOG.md))

---

## 1. Objective
Stabilize the Attempt 0 baseline by fixing its five concrete runtime/boundary bugs, attempt a first **naive object-oriented refactor** (while still keeping matrix-backed definitions and Tkinter structure), verify end-to-end gameplay via headless smoke tests, and audit the result against `PoPL2026AssignmentExTetris.pdf` (Section 3.2) and the target architecture to expose where the matrix-wrapper approach falls short.

## 2. Files Modified in `attempts/attempt_1_naive_oop/`
| File | Key Changes Over Attempt 0 |
|------|----------------------------|
| `board.py` | Explicit bounds checking in `Board.collision()` rejecting negative indices `(0, -1)` / `(-1, 0)` instead of wrapping around. |
| `shape.py` | Non-mutable `mat=None` default, defensive `.copy()` in `Shape.__init__` and `transpose()`, `clone()`, `bounding_box()`, plus `ClassicTetromino` and `ExtendedTetromino` subclasses. |
| `allextetrominoes.py` | Removed 73 `Extetromino*` globals and `eval()`; introduced `PieceRegistry` deduplicating `[1, 10, 11]` down to **71** unique oriented matrices (`7` Classic + `64` Extended). |
| `engine.py` | Added explicit `import numpy` and `simpledialog`; fixed `self.pasueStatus` typo and `game_over_status` updates; removed `eval()` in `__main__`; moved `after()`/`mainloop()` into `run()`; added `headless=False` mode and `self.piece.clone()` on rotations. |

## 3. Verification & Observed Results

### A. Bug-Fix Checks (`INT-002`)
`python3 -m py_compile *.py` and AST/runtime assertions passed:
- Explicit `numpy` and `simpledialog` imports verified; zero `Extetromino*` globals and zero executable `eval()` calls.
- `Shape()` default no longer shares mutable state across instances; `Shape.fliplr()` no longer mutates registry matrices.
- `Board.collision` returns `True` for `(0, -1)`, `(-1, 0)`, `(0, 7)`, and `(20, 0)`, and `False` for `(0, 6)`.
- Out-of-range lookup `get_extetromino_at(99)` raises `ValueError`.

### B. Registry & Rotation Invariance (`INT-003`)
- All **71** deduplicated matrices matched Attempt 0's unique matrix set identically (`7` `ClassicTetromino` + `64` `ExtendedTetromino`).
- All 71 pieces passed `CW + AntiCW` and `4 × CW` rotation invariance while preserving subclass type via `clone()`.
- `python3 shape.py` exited cleanly (`934` lines printed).

### C. Headless Gameplay Smoke Tests (`INT-004`)
```text
SMOKE 1 PASS: Movement & wall boundaries OK, rightmost cursor = (0, 6)
SMOKE 2 PASS: CW/CCW rotation, subclass preservation & collision rejection OK
SMOKE 3 PASS: Pause/resume input gating OK
SMOKE 4 PASS: Line clearing OK, deleted_lines = 1
SMOKE 5 PASS: Game-over detection & new_game() reset OK
```

### D. Combinatorial & Section 3.2 Audit (`INT-005`)
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
  Attempt 1 groups that are rotations of the same one-sided polyplet: 21 groups
```

## 4. Shortcomings & Trade-Offs (Motivating Attempt 2 & Attempt 3)
1. **Still Matrix-Initialized (Violates Section 3.2):** Pieces are still defined via hard-coded boolean matrices (`_CLASSIC_SPECS` / `_EXTENDED_SPECS`) rather than parameterized geometric constructors.
2. **Incomplete & Biased Catalog:** Covers `71 / 110` fixed 4-polyplets (missing 39) while containing **21 redundant rotation-equivalent groups**, which silently biases uniform sampling toward shapes that appear in multiple rotations.
3. **Missing Classification Axes:** `ClassicTetromino` and `ExtendedTetromino` are marker subclasses without bounding-box classes (notably including `(3, 4)` and `(4, 3)`), morphology classes (`OrthogonalTetromino` vs. `DiagonalPolyplet`), or landing-cavity classes (`FlatLandingShape`, `SingleCavityShape`, `MultiCavityShape`).
4. **Crude Probability & Coupled Engine:** `get_any_piece()` still samples by index sequence; Tkinter remains imported and interleaved inside `TetrisEngine`; and there is no FSM, Observer API, Board metrics, or no-code designer configuration layer.
