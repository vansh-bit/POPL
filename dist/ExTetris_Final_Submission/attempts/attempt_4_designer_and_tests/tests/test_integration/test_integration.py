import contextlib
import io
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = str(Path(__file__).resolve().parents[2])
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from builder import load_game_from_json
import play
from renderers import CLIRenderer, TkinterRenderer


class TestIntegrationWorkflows(unittest.TestCase):
    def test_headless_and_cli_workflows(self):
        eng, hr = load_game_from_json(Path(ROOT) / "configs" / "custom.json")
        frames = hr.run(eng, steps=5, action_sequence=["LEFT", "CW", "HARD_DROP", "STEP"])
        self.assertGreaterEqual(len(frames), 4)
        self.assertGreater(eng.score, 0)

        buf = io.StringIO()
        cli = CLIRenderer(stream=buf, use_ansi=True, tick_sleep=0.005)
        eng2, _ = load_game_from_json(Path(ROOT) / "configs" / "classic.json")
        cli.run(eng2, max_ticks=1)
        self.assertIn("ExTetris | State: RUNNING", buf.getvalue())

        stdout_cap = io.StringIO()
        with contextlib.redirect_stdout(stdout_cap):
            rc = play.main(["--config", str(Path(ROOT) / "configs" / "custom.json"), "--steps", "6"])
        self.assertEqual(rc, 0)
        self.assertIn("Captured 7 headless frames", stdout_cap.getvalue())

    def test_optional_tk_renderer(self):
        if TkinterRenderer.is_available():
            tk_r = TkinterRenderer()
            eng, _ = load_game_from_json(Path(ROOT) / "configs" / "classic.json")
            tk_r.render(eng)
            tk_r.close()

    def test_notebook_workflow_executes_cleanly(self):
        nb_path = Path(ROOT) / "ExTetris_Studio.ipynb"
        self.assertTrue(nb_path.exists())
        proc = subprocess.run(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "notebook",
                "--execute",
                "--stdout",
                str(nb_path),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("Studio Custom Diagonal Variant", proc.stdout)
