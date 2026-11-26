# packaging.py: Reproducible submission ZIP packager
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from pathlib import Path
import sys
import zipfile


INCLUDE_ROOTS = (
    "extetris",
    "configs",
    "tests",
    "docs",
    "attempts",
    "ExTetris_Studio.ipynb",
    "AI_INTERACTION_LOG.md",
    "Makefile",
    "setup.sh",
    "run.sh",
    "test.sh",
    "LICENSE",
    "README.md",
    "pyproject.toml",
)

SKIP_DIR_NAMES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "dist",
    "build",
}
SKIP_SUFFIXES = {".pyc", ".pyo"}
SKIP_FILENAMES = {".DS_Store", "answers.txt"}


def build_submission_zip(root_dir=None, output_path=None):
    root = Path(root_dir).resolve() if root_dir is not None else Path.cwd().resolve()
    out = Path(output_path).resolve() if output_path is not None else root / "dist" / "extetris_submission.zip"
    out.parent.mkdir(parents=True, exist_ok=True)

    count = 0
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for item in INCLUDE_ROOTS:
            target = root / item
            if not target.exists():
                continue
            if target.is_file():
                if target.name not in SKIP_FILENAMES:
                    zf.write(target, target.relative_to(root).as_posix())
                    count += 1
            else:
                for path in sorted(target.rglob("*")):
                    if not path.is_file():
                        continue
                    rel = path.relative_to(root)
                    if any(part in SKIP_DIR_NAMES or part.endswith(".egg-info") for part in rel.parts):
                        continue
                    if path.suffix in SKIP_SUFFIXES or path.name in SKIP_FILENAMES:
                        continue
                    zf.write(path, rel.as_posix())
                    count += 1

    return out, count


def main(argv=None):
    out, count = build_submission_zip()
    print(f"Created {out} ({count} files, {out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
