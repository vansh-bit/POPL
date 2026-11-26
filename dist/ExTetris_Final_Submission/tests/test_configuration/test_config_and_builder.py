from pathlib import Path
import tempfile
import unittest

from extetris import ConfigValidationError, ExTetrisBuilder, load_config, load_game_from_json, validate_config


ROOT = Path(__file__).resolve().parents[2]


class TestConfigurationAndBuilder(unittest.TestCase):
    def test_all_presets_load_and_build(self):
        for name in ("classic.json", "extended.json", "chaos.json", "custom.json"):
            cfg = load_config(ROOT / "configs" / name)
            self.assertIn("variant", cfg)
            eng, rend = load_game_from_json(ROOT / "configs" / name)
            self.assertEqual(eng.width, cfg["board"]["width"])
            self.assertEqual(eng.height, cfg["board"]["height"])
            rend.close()

    def test_invalid_configurations_raise_clear_errors(self):
        bad_cases = [
            {"board": {"width": 2, "height": 20}},
            {"board": {"width": 10, "height": 100}},
            {"variant": "invalid_mode"},
            {"distribution": {"strategy": "quantum"}},
            {"renderer": "opengl"},
            {"max_holes": -1},
            {"max_holes": True},
            {"gameplay": {"initial_speed_ms": 50}},
            {"gameplay": {"speed_factor": 1.5}},
            {"distribution": {"seed": "bad"}},
            {"distribution": {"seed": False}},
            {"widht": 10},
            {"variant": "classic", "connectivity": "diagonal"},
            {"distribution": {"strategy": "weighted", "weights_by_id": {"1": -1}}},
        ]
        for bad in bad_cases:
            with self.assertRaises(ConfigValidationError):
                validate_config(bad)

        with tempfile.TemporaryDirectory() as tmp:
            broken = Path(tmp) / "broken.json"
            broken.write_text("{ bad json", encoding="utf-8")
            with self.assertRaises(ConfigValidationError):
                load_config(broken)
            with self.assertRaises(ConfigValidationError):
                load_config(Path(tmp) / "does_not_exist.json")

    def test_builder_chaining_and_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "exported"
            info = (
                ExTetrisBuilder()
                .with_name("Builder Test Variant")
                .use_extended_tetris()
                .filter_diagonal_only()
                .filter_max_holes(2)
                .with_board_size(12, 22)
                .with_distribution("bag", seed=42)
                .with_renderer("headless")
                .export_variant(out)
            )
            self.assertTrue(info["config"].exists())
            self.assertTrue(info["docs"].exists())
            self.assertTrue(info["launcher"].exists())
            self.assertGreater(info["piece_count"], 0)

        with self.assertRaises(ConfigValidationError):
            ExTetrisBuilder().use_classic_tetris().filter_by(lambda _p: False).build()
