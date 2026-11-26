# ExTetris Game Programmer's Manual (No-Code Variant Guide)

Welcome! This manual is written for **game designers** who want to create, customize, play, and release their own Extended Tetris (ExTetris) variant **without writing Python code**.

---

## 1. Quick Start (Installation & Ready-Made Presets)

- **Normal installation (requires internet/PyPI):** Installs ExTetris and required packages (`numpy`):
  ```bash
  ./setup.sh          # or: ./setup.sh --venv   (recommended isolated environment)
  ```
- **Offline installation (no internet):** Uses already-installed system/environment packages (`pip install --no-build-isolation --no-deps -e .`). Ensure `setuptools`, `wheel`, and `numpy` are already installed before running:
  ```bash
  ./setup.sh --offline
  ```

After setup, you can launch any included preset immediately:

| Command | Variant | Piece Pool | Board | Strategy |
|---------|---------|------------|-------|----------|
| `make run-classic` | Classic Tetris | 7 standard tetrominoes | `10×20` | 7-Bag |
| `make run-extended` | Extended Polyplet Tetris | 34 one-sided shapes ($\le 4$ holes) | `12×22` | Adaptive Difficulty |
| `make run-chaos` | Chaos ExTetris | All 110 fixed 4-polyplets | `14×24` | Markov anti-repeat |
| `make run-gui` | Extended GUI | 34 one-sided shapes | `12×22` | Adaptive (Tkinter window) |
| `./run.sh --config configs/custom.json` | Gentle Diagonal | Diagonal shapes ($\le 2$ holes) | `10×20` | Seeded Bag |

### In-Game Controls
- **Move Left / Right:** `a` / `d` or `←` / `→`
- **Rotate Clockwise / Counter-Clockwise:** `w` or `↑` (CW), `e` (CCW)
- **Soft Drop / Hard Drop:** `s` or `↓` (soft), `Space` (instant drop)
- **Pause / Resume:** `p`
- **Quit:** `q`

---

## 2. Method A — Design a Variant Visually with `ExTetris_Studio.ipynb` (Recommended)

Open [ExTetris_Studio.ipynb](../ExTetris_Studio.ipynb) in Jupyter (`jupyter notebook ExTetris_Studio.ipynb` or VS Code / JupyterLab):

1. **Inspect Pieces:** Run the catalog cells to see all **110** shapes grouped by bounding box (`1×4` through `4×4`, including `3×4` and `4×3`), edge vs. corner connectivity, and landing-hole difficulty.
2. **Use the Interactive Sliders & Dropdowns:**
   - **Variant:** `classic`, `extended`, `chaos`, or `custom`
   - **Scope:** `one_sided` (34 unique shapes) or `fixed` (all 110 orientations)
   - **Connect:** `any`, `orthogonal` (classic edges only), or `diagonal` (corner-connected only)
   - **Max Holes (`0..6`):** Cap how many overhanging cavities a piece can create when landing (`0` = flat pieces only, easier; `3..6` = much harder)
   - **Width / Height & Speed:** Adjust board dimensions and starting drop interval (ms)
   - **Dist:** Choose `uniform`, `bag` (fair shuffling), `adaptive` (helps when your stack gets tall/holey), or `markov` (avoids repeats)
3. **Preview & Export:** Run the preview and export cells to generate a ready-to-share variant folder containing `variant_config.json`, `VARIANT_README.md`, and `run_variant.py`.

---

## 3. Method B — Create a Variant by Editing a JSON File

Copy `configs/custom.json` to `configs/my_game.json` and edit any values in a plain text editor:

```json
{
  "name": "My Fast Classic-Plus",
  "description": "Classic pieces plus gentle diagonal pieces, starting fast.",
  "variant": "extended",
  "piece_scope": "one_sided",
  "connectivity": "any",
  "max_holes": 2,
  "board": {
    "width": 10,
    "height": 20
  },
  "gameplay": {
    "initial_speed_ms": 650,
    "speed_factor": 0.90,
    "enable_wall_kicks": true,
    "enable_ghost": true
  },
  "distribution": {
    "strategy": "bag",
    "bag_multiplier": 1,
    "seed": 2026
  },
  "renderer": "cli"
}
```

### What Each Setting Controls
- `variant` + `piece_scope`:
  - `"classic"` (`one_sided` = 7 pieces; `fixed` = 19)
  - `"extended"` / `"chaos"` / `"custom"` (`one_sided` = 34; `fixed` = 110)
- `connectivity`: `"any"`, `"orthogonal"` (edge-connected only), or `"diagonal"` (corner-connected only). *(Note: `"classic"` cannot be combined with `"diagonal"`.)*
- `max_holes`: `null` (no limit) or `0..6`.
- `board.width`: integer `4..40`; `board.height`: integer `6..60`.
- `gameplay.initial_speed_ms`: integer `100..5000`; `speed_factor`: `(0.1, 1.0]` (applied every 10 cleared lines, minimum interval `100 ms`).
- `distribution.strategy`: `"uniform"`, `"weighted"` (optional `weights_by_id`), `"bag"`, `"adaptive"`, or `"markov"`.
- `renderer`: `"cli"` (terminal), `"tk"` (desktop window), or `"headless"` (automated simulation).

If you make a typo or enter an impossible setting, ExTetris prints a clear `Invalid ExTetris configuration` message telling you the exact field and valid range.

---

## 4. Releasing Your Variant with Documentation

Run one command to test or package your JSON config into a standalone release directory (including `variant_config.json`, auto-generated `VARIANT_README.md`, and `run_variant.py`):

```bash
./run.sh --config configs/my_game.json --export releases/my_game
```

Anyone can then read `releases/my_game/VARIANT_README.md` and launch your game with:

```bash
python3 releases/my_game/run_variant.py
```
