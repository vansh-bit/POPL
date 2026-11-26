import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import venv
import zipfile

from extetris.packaging import build_submission_zip


ROOT = Path(__file__).resolve().parents[2]


class TestSubmissionPackage(unittest.TestCase):
    def test_clean_venv_install_tests_cli_and_config(self):
        if os.environ.get("EXTETRIS_SKIP_PACKAGING_TEST") == "1":
            self.skipTest("Skipping recursive packaging test inside clean venv.")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            zip_path = tmp_path / "extetris_submission.zip"

            # 1. Build submission ZIP
            out_zip, file_count = build_submission_zip(root_dir=ROOT, output_path=zip_path)
            self.assertTrue(out_zip.exists())
            self.assertGreater(file_count, 50)

            # 2. Extract into temporary directory
            extract_dir = tmp_path / "extracted"
            with zipfile.ZipFile(out_zip, "r") as zf:
                zf.extractall(extract_dir)
            self.assertTrue((extract_dir / "pyproject.toml").exists())
            self.assertTrue((extract_dir / "configs" / "classic.json").exists())
            self.assertTrue((extract_dir / "README.md").exists())
            self.assertTrue((extract_dir / "README.pdf").exists())
            self.assertTrue((extract_dir / "AI_INTERACTION_LOG.md").exists())
            self.assertTrue((extract_dir / "AI_INTERACTION_LOG.pdf").exists())
            self.assertTrue((extract_dir / "GIT_HISTORY.txt").exists())
            self.assertTrue((extract_dir / "docs" / "AI_USAGE_REPORT.md").exists())
            self.assertTrue((extract_dir / "docs" / "AI_USAGE_REPORT.pdf").exists())
            self.assertTrue((extract_dir / "docs" / "UML.pdf").exists())
            diagrams_dir = extract_dir / "docs" / "diagrams"
            self.assertTrue(diagrams_dir.is_dir())
            for diag_name in (
                "class_hierarchy.svg",
                "class_hierarchy.png",
                "fsm_states.svg",
                "fsm_states.png",
                "sequence_game_loop.svg",
                "sequence_game_loop.png",
            ):
                self.assertTrue((diagrams_dir / diag_name).exists(), f"Missing diagram {diag_name}")

            # 3. Create clean virtual environment and pip install extracted project
            venv_dir = tmp_path / "venv"
            venv.create(venv_dir, with_pip=True, system_site_packages=False)
            bin_dir = venv_dir / ("Scripts" if sys.platform == "win32" else "bin")
            venv_python = bin_dir / ("python.exe" if sys.platform == "win32" else "python")
            venv_pip = bin_dir / ("pip.exe" if sys.platform == "win32" else "pip")
            venv_cli = bin_dir / ("extetris.exe" if sys.platform == "win32" else "extetris")

            clean_env = {
                k: v for k, v in os.environ.items()
                if k not in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV")
            }
            clean_env["PATH"] = f"{bin_dir}{os.pathsep}{clean_env.get('PATH', '')}"

            install_proc = subprocess.run(
                [str(venv_pip), "install", str(extract_dir)],
                cwd=str(extract_dir),
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=180,
            )
            if install_proc.returncode != 0:
                combined_err = f"{install_proc.stdout}\n{install_proc.stderr}"
                offline_markers = (
                    "NewConnectionError",
                    "ConnectionError",
                    "NameResolutionError",
                    "Temporary failure in name resolution",
                    "nodename nor servname",
                    "ProxyError",
                    "ReadTimeoutError",
                    "Could not find a version that satisfies",
                    "No matching distribution found",
                    "Cannot fetch index",
                )
                if any(marker in combined_err for marker in offline_markers):
                    self.skipTest(
                        "Offline environment: pip could not download build/runtime dependencies into isolated venv."
                    )
                self.fail(
                    f"pip install failed:\nSTDOUT:\n{install_proc.stdout}\nSTDERR:\n{install_proc.stderr}"
                )
            self.assertTrue(venv_cli.exists(), "extetris console entrypoint not created in clean venv")

            # 4. Run full unit/integration test suite inside clean venv (skipping recursive packaging)
            test_env = dict(clean_env)
            test_env["EXTETRIS_SKIP_PACKAGING_TEST"] = "1"
            test_proc = subprocess.run(
                [str(venv_python), "-m", "unittest", "discover", "-s", "tests", "-t", ".", "-v"],
                cwd=str(extract_dir),
                env=test_env,
                capture_output=True,
                text=True,
                timeout=120,
            )
            self.assertEqual(
                test_proc.returncode,
                0,
                msg=f"Clean-venv tests failed:\n{test_proc.stdout}\n{test_proc.stderr}",
            )

            # 5. Launch a basic game variant via installed extetris CLI
            cli_proc = subprocess.run(
                [str(venv_cli), "--config", "configs/custom.json", "--steps", "6"],
                cwd=str(extract_dir),
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=60,
            )
            self.assertEqual(cli_proc.returncode, 0, msg=cli_proc.stderr)
            self.assertIn("Captured 7 headless frames", cli_proc.stdout)

            # 6. Load & validate JSON config inside clean venv (from outside extract_dir to verify true install)
            cfg_check = subprocess.run(
                [
                    str(venv_python),
                    "-c",
                    (
                        "import extetris; "
                        f"cfg = extetris.load_config({str(extract_dir / 'configs' / 'extended.json')!r}); "
                        "assert cfg['variant'] == 'extended' and cfg['board']['width'] == 12; "
                        "print('CLEAN_VENV_IMPORT_PATH=', extetris.__file__)"
                    ),
                ],
                cwd=str(tmp_path),
                env=clean_env,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(cfg_check.returncode, 0, msg=cfg_check.stderr)
            self.assertIn(str(venv_dir.resolve()), str(Path(cfg_check.stdout.split("=", 1)[1].strip()).resolve()))
