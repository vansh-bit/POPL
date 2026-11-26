from pathlib import Path
import tempfile
import unittest
import numpy as np

from extetris import ExTetrisEngine, GameState, PersistenceError, load_game_from_json


ROOT = Path(__file__).resolve().parents[2]


class TestPersistence(unittest.TestCase):
    def test_save_load_and_bit_identical_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            save_path = Path(tmp) / "state.json"
            txt_path = Path(tmp) / "board.txt"
            eng, _ = load_game_from_json(ROOT / "configs" / "custom.json")
            eng.start()
            eng.move_left()
            eng.soft_drop()
            eng.hard_drop()
            eng.pause()
            eng.save_state(save_path)
            eng.export_text_board(txt_path)
            self.assertTrue(save_path.exists())
            self.assertTrue(txt_path.exists())

            restored = ExTetrisEngine.load_state(save_path)
            self.assertEqual(restored.state, GameState.PAUSED)
            self.assertEqual(restored.score, eng.score)
            self.assertEqual(restored.cursor, eng.cursor)
            self.assertEqual(restored.current_piece.coords, eng.current_piece.coords)
            self.assertEqual(restored.next_piece.coords, eng.next_piece.coords)
            self.assertTrue(np.array_equal(restored.board.area, eng.board.area))

            eng.resume()
            restored.resume()
            for method in ("hard_drop", "move_left", "rotate_cw", "hard_drop", "hard_drop"):
                getattr(eng, method)()
                getattr(restored, method)()
            self.assertEqual(eng.score, restored.score)
            self.assertEqual(eng.current_piece.coords, restored.current_piece.coords)
            self.assertEqual(eng.next_piece.coords, restored.next_piece.coords)
            self.assertTrue(np.array_equal(eng.board.area, restored.board.area))

    def test_corrupt_or_missing_save_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(PersistenceError):
                ExTetrisEngine.load_state(Path(tmp) / "missing.json")
            bad = Path(tmp) / "bad.json"
            bad.write_text('{"format": "unknown"}', encoding="utf-8")
            with self.assertRaises(PersistenceError):
                ExTetrisEngine.load_state(bad)
