# Continued Development & AI Usage Report (Section 2.2)

- **Project:** Extended Tetris (ExTetris) — CS F301 PoPL, Sem-I, 2026-27
- **Primary AI Assistant Used:** Antigravity (Gemini 4 Hydrogen High / Gemini 3.8 Flash High)
- **Complete Verbatim Log:** [../AI_INTERACTION_LOG.md](../AI_INTERACTION_LOG.md) (`INT-001` through `INT-027` — verbatim prompts & verbatim AI responses separated from terminal outputs)
- **Preserved Historical Snapshots:** [../attempts/README.md](../attempts/README.md) (`attempt-0-baseline` through `attempt-5-final`)

---

## 1. Development Methodology & Preservation of All Attempts
Rather than jumping straight to a finished codebase or discarding flawed drafts, ExTetris was developed across **six progressive, runnable snapshots (Attempts 0–5)**. Every earlier attempt is preserved on disk in `attempts/` (`attempt_0_appendix_baseline/` through `attempt_4_designer_and_tests/`), and every prompt, verbatim AI response, observed failure, manual diagnosis, and architectural trade-off is recorded chronologically in [../AI_INTERACTION_LOG.md](../AI_INTERACTION_LOG.md).

> **Note on Git References vs. Submission ZIP:**  
> Commit hashes (`846e81b`, `9e2cfc7`, `31ed371`, `c091859`, `c18c89a`, `8282631`) and tags (`attempt-0-baseline`..`attempt-5-final`) come from the **local Git repository** used during development (no remote repository URL is configured). *(Historical intermediate Attempt 5 commits `3d59b1c`, `cfd1a1f`, `fa26c1f`, `fdb216c` remain ancestors in local Git history; the final `attempt-5-final` tag resolves to `8282631`.)* The submission ZIP omits `.git/` metadata by design to stay lightweight and reproducible, while preserving all historical Attempt 0–4 source trees and reports independently on disk under `attempts/`.

### Installation Modes (Online vs. Offline)
- **Normal installation** (`./setup.sh`, `make setup`, or `./setup.sh --venv`): executes `pip install -e .` and installs declared dependencies (`numpy`, etc.).
- **Offline installation** (`./setup.sh --offline` or `./setup.sh --venv --offline`): executes `pip install --no-build-isolation --no-deps -e .`, skipping network resolution and therefore **requiring build/runtime dependencies (`setuptools`, `wheel`, `numpy`) to already be preinstalled** in the target Python environment.

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
- **Post-Audit Fixes (`INT-027`):** Caught and fixed three portability/testing issues during final audit: (1) `TkinterRenderer.is_available()` now probes opening a `Tk()` window so headless systems return `False` and `test_optional_tk_renderer` reports `SKIPPED` instead of failing; (2) `setup.sh` now runs `pip install -e .` (reserving `--no-deps` for explicit `--offline` mode) so dependencies like `numpy` install cleanly in a fresh `.venv`; and (3) `test_submission_package.py` skips cleanly when `pip` cannot reach PyPI in an offline environment while still failing on genuine packaging errors. Synced `extetris/cli.py` preset defaults with `configs/*.json`.

---

## 3. Effort Comparison: With AI Assistance vs. Without AI Assistance

> **Methodological Qualification (Retrospective Estimates vs. Measured Facts):**  
> The session spanned from `01:55 IST` (`INT-001` workspace setup/baseline) to `12:50 IST` (`INT-027` post-audit fixes) on 26 November 2026 with intermittent user breaks between phases. Neither the active with-AI effort (~2.75 hours across active coding/verification windows) nor the without-AI baseline (**~22–33 hours**, implying roughly an **~8–12× speedup**) comes from a controlled experiment building the codebase twice. Both figures are **retrospective engineering estimates** grounded in transcript timestamps, codebase size, debugging incidents logged in `AI_INTERACTION_LOG.md`, and typical manual implementation effort for software of comparable scope.

### Breakdown & Estimation Basis

| Activity / Phase | Est. Active Effort (With AI) | Est. Manual Effort (Without AI) | Basis for Manual Estimate | Accelerated by AI | Required Independent Research, Debugging & Human Judgment |
|------------------|------------------------------|---------------------------------|---------------------------|-------------------|-------------------------------------------------------------|
| **Starter Baseline Audit & Bug Hunting** (Attempts 0–1) | ~20 min | ~2–3 hours | Manual PDF transcription, reproducing UI freezes, and tracing NumPy/Tkinter quirks | Initial boilerplate extraction and AST/import probe scripts | Diagnosing silent negative-index wrap-around in `Board.collision()`, `tk.simpledialog` implicit submodule import behavior, preserving Attempt 0 unmodified, and proving why 71 matrices biased sampling (`INT-001`–`INT-005`) |
| **Combinatorial 4-Polyplet Math & Multi-Axis Hierarchy** (Attempt 2) | ~25 min | ~4–6 hours | Deriving 8-connectivity invariants, symmetry canonicalization, MRO composition, and unit tests | Enumerating candidate hierarchy classes and rotation-invariant test cases | Verifying the exact `110` fixed / `34` one-sided / `22` free / `7` classic counts, designing cooperative `(Box, Morphology, Cavity)` synthesis over 66 manual classes, catching `Shape.clone()` dropping subclasses on rotation, and fixing the full-row blocker bug in the Attempt 2 game-over test (`INT-007`–`INT-010`) |
| **FSM Engine, Functional-OO Distributions & Renderers** (Attempt 3) | ~35 min | ~6–8 hours | Implementing decoupled FSM states, wall-kick tables, cross-platform `termios`/`msvcrt` I/O, and 5 composable distributions | Multi-strategy class scaffolding, combinator adapters, and repetitive test setup | Enforcing zero `tkinter` leakage into core engine, designing seeded combinator reproducibility invariants, catching IEEE-754 `math.ceil(450 * 1.1)` float drift (`496` vs `495`), and isolating `termios.setcbreak()` behind `isatty()` (`INT-012`–`INT-015`) |
| **JSON Schema, Builder, Persistence, Studio Notebook & Tests** (Attempt 4) | ~45 min | ~6–10 hours | Authoring JSON schema rules, Fluent Builder, stateful save/load parity, Jupyter widgets, and 8 test suites | Drafting repetitive validator branches, JSON presets, notebook cell scaffolding, and categorized tests | Catching `_is_strict_int()` boolean trap (`isinstance(True, int)`), diagnosing premature `BagDistribution` draws during `load_engine_state()`, fixing row `10` vs row `8` wall-kick test fixture, and enforcing zero duplicate game rules in `ExTetris_Studio.ipynb` (`INT-017`–`INT-020`) |
| **Packaging, Clean-Venv Verification, Docs & Final Audit** (Attempt 5) | ~40 min | ~4–6 hours | Setting up `pyproject.toml`, Make/shell automation, Mermaid UML/API/designer manuals, and clean-venv release testing | Structuring Markdown/Mermaid documentation and packaging/CLI boilerplate | Debugging Make backslash `SyntaxError` (extracting `extetris/packaging.py`), enforcing isolated `venv` verification, probing `Tk()` display availability (`INT-027`), fixing `setup.sh --no-deps` dependency omission, adding offline pip skip detection, and preserving authentic verbatim logs (`INT-022`–`INT-027`) |
| **Retrospective Total** | **~2.75 hours** | **~22–33 hours** | Sum of phase estimates | **~8–12× estimated speedup** on scaffolding, repetitive tests & docs | **All architecture boundaries, correctness audits, bug diagnoses, and assignment alignment depended on human verification** |

### Candid Assessment of Trade-Offs
- **What AI Actually Accelerated:** Rapid iteration across six complete runnable snapshots, generating structured multi-axis test matrices, drafting JSON schema presets, and formatting technical/UML/designer documentation.
- **What Required Human Verification & Debugging:** Every single AI-generated phase required hands-on execution, review, and manual course-correction—AI test fixtures initially contained real logic errors (Attempt 2 full-row blocker self-clearing, Attempt 4 wrong wall-kick obstacle row), `load_engine_state()` silently broke bag parity until initialization order was corrected, inline Make Python raised `SyntaxError`, and `TkinterRenderer.is_available()`/`setup.sh`/`test_submission_package.py` initially hid headless and offline environment assumptions until explicitly audited (`INT-027`).
