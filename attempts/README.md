# Development Attempts Archive

This directory preserves every earlier runnable attempt of the ExTetris assignment so that no intermediate or less-successful design is discarded.

> **Important Note on Attempt 5 & Git Metadata:**  
> The final verified release (**Attempt 5**) lives directly in the repository root (`extetris/`, `configs/`, `tests/`, `docs/`, `ExTetris_Studio.ipynb`, `Makefile`, `pyproject.toml`) rather than duplicated inside `attempts/`. Commit hashes and tags listed below refer to the **local development Git repository** (no remote repository URL is configured). Submission ZIP archives omit `.git/` metadata by design while preserving every runnable historical snapshot (Attempts 0–4) directly on disk inside `attempts/`. See GIT_HISTORY.txt for the git log these hashes come from.

## Attempt Progression & Git Mapping

| Attempt | Directory / Location | Goal & Focus | Git Commit / Tag | Report |
|---------|----------------------|--------------|------------------|--------|
| **Attempt 0** | `attempts/attempt_0_appendix_baseline/` | Faithful reproduction of Appendix A–D (`engine.py`, `board.py`, `shape.py`, `allextetrominoes.py`) + observed crashes | `846e81b` (`attempt-0-baseline`) | [ATTEMPT_0_REPORT.md](./attempt_0_appendix_baseline/ATTEMPT_0_REPORT.md) |
| **Attempt 1** | `attempts/attempt_1_naive_oop/` | Minimal fixes to run + initial naive OOP refactor | `9e2cfc7` (`attempt-1-naive-oop`) | [ATTEMPT_1_REPORT.md](./attempt_1_naive_oop/ATTEMPT_1_REPORT.md) |
| **Attempt 2** | `attempts/attempt_2_shape_hierarchy/` | Coordinate-based `Shape` hierarchy, 110 canonical 4-polyplets, bounding boxes (incl. 3×4, 4×3), morphology & landing cavities | `31ed371` (`attempt-2-shape-hierarchy`) | [ATTEMPT_2_REPORT.md](./attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md) |
| **Attempt 3** | `attempts/attempt_3_engine_and_distributions/` | UI-agnostic FSM `ExTetrisEngine`, Functional-OO `ShapeDistribution`, Observer callbacks, `Headless`/`CLI` renderers (Tkinter optional) | `c091859` (`attempt-3-engine-and-distributions`) | [ATTEMPT_3_REPORT.md](./attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md) |
| **Attempt 4** | `attempts/attempt_4_designer_and_tests/` | `ExTetrisBuilder`, JSON config validation, no-code `ExTetris_Studio.ipynb`, initial full test suite (incl. invalid configs) | `c18c89a` (`attempt-4-designer-and-tests`) | [ATTEMPT_4_REPORT.md](./attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md) |
| **Attempt 5** | Root (`extetris/`, `configs/`, `tests/`, `docs/`, `dist/`) | Final verified release, packaging verification, complete manuals & `AI_USAGE_REPORT.md` | `8282631` (`attempt-5-final`) | [docs/AI_USAGE_REPORT.md](../docs/AI_USAGE_REPORT.md) |
