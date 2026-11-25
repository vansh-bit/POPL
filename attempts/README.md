# Development Attempts Archive

This directory preserves every earlier runnable attempt of the ExTetris assignment so that no intermediate or less-successful design is discarded.

> **Important Note on Attempt 5:**  
> The final verified release (**Attempt 5**) lives directly in the repository root (`extetris/`, `configs/`, `tests/`, `docs/`, `ExTetris_Studio.ipynb`, `Makefile`, `pyproject.toml`) rather than duplicated inside `attempts/`. When verified, it is tagged in Git as `attempt-5-final`.

## Attempt Progression & Git Mapping

| Attempt | Directory / Location | Goal & Focus | Git Commit / Tag | Report |
|---------|----------------------|--------------|------------------|--------|
| **Attempt 0** | `attempts/attempt_0_appendix_baseline/` | Faithful reproduction of Appendix A–D (`engine.py`, `board.py`, `shape.py`, `allextetrominoes.py`) + observed crashes | `846e81b` (`attempt-0-baseline`) | [ATTEMPT_0_REPORT.md](./attempt_0_appendix_baseline/ATTEMPT_0_REPORT.md) |
| **Attempt 1** | `attempts/attempt_1_naive_oop/` | Minimal fixes to run + initial naive OOP refactor | *(pending)* | [ATTEMPT_1_REPORT.md](./attempt_1_naive_oop/ATTEMPT_1_REPORT.md) |
| **Attempt 2** | `attempts/attempt_2_shape_hierarchy/` | Coordinate-based `Shape` hierarchy, 110 canonical 4-polyplets, bounding boxes (incl. 3×4, 4×3), morphology & landing cavities | *(pending)* | [ATTEMPT_2_REPORT.md](./attempt_2_shape_hierarchy/ATTEMPT_2_REPORT.md) |
| **Attempt 3** | `attempts/attempt_3_engine_and_distributions/` | UI-agnostic FSM `ExTetrisEngine`, Functional-OO `ShapeDistribution`, Observer callbacks, `Headless`/`CLI` renderers (Tkinter optional) | *(pending)* | [ATTEMPT_3_REPORT.md](./attempt_3_engine_and_distributions/ATTEMPT_3_REPORT.md) |
| **Attempt 4** | `attempts/attempt_4_designer_and_tests/` | `ExTetrisBuilder`, JSON config validation, no-code `ExTetris_Studio.ipynb`, initial full test suite (incl. invalid configs) | *(pending)* | [ATTEMPT_4_REPORT.md](./attempt_4_designer_and_tests/ATTEMPT_4_REPORT.md) |
| **Attempt 5** | Root (`extetris/`, `configs/`, `tests/`, `docs/`, `dist/`) | Final verified release, packaging verification, complete manuals & `AI_USAGE_REPORT.md` | *(pending `attempt-5-final`)* | [docs/AI_USAGE_REPORT.md](../docs/AI_USAGE_REPORT.md) |
