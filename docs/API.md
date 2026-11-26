# ExTetris API Reference (Application Programmer's Manual)

All public symbols are re-exported from the top-level package `extetris` (`import extetris`) as well as their dedicated subpackages.

---

## 1. Shapes & Polyplet Factory (`extetris.shapes`)

### `normalize_coords(coords) -> tuple[tuple[int, int], ...]`
Translates an iterable of `(r, c)` coordinates so `min_r == 0` and `min_c == 0`, returning a sorted tuple. Raises `ValueError` on empty input or duplicate cells.

### `is_connected(coords, diagonal=True) -> bool`
Checks single-component connectivity using 8-neighborhood (`diagonal=True`) or 4-neighborhood (`diagonal=False`) BFS.

### `class Shape(coords=None, piece_id=None, name=None)`
- `coords`: normalized tuple of `(r, c)` cells (defaults to `1×4` bar).
- `bounding_box() -> (height, width)` / `.height` / `.width`
- `rotateCW() -> self` / `rotateAntiCW() -> self` / `fliplr() -> self` / `flipud() -> self`: affine grid transforms anchored at `(0, 0)`.
- `to_matrix() -> numpy.ndarray` (also `.matrix` property): materializes a 2D boolean array on demand.
- `landing_holes() -> int`: counts empty bounding-box cells trapped strictly below an occupied cell in the same column.
- `landing_hole_profile() -> tuple[int, int, int, int]`: `(h0, h90, h180, h270)` across all 4 clockwise rotations.
- `min_landing_holes() -> int`, `max_landing_holes() -> int`, `clone() -> Shape`.

### `class ExTetromino(Shape)`
Enforces `len(coords) == 4` and 8-connectivity.
- `is_orthogonal() -> bool`: `True` iff 4-connected.
- `is_diagonal() -> bool`: `True` iff at least one corner-only link is required.
- `canonical_one_sided() -> tuple`: minimum normalized coords across 4 rotations.
- `canonical_free() -> tuple`: minimum normalized coords across rotations and reflections.

### Multi-Axis Subclasses (`extetris.shapes.hierarchy`)
- **Bounding Box (`BOUNDING_BOX_CLASSES`):** `Box1x4Shape`, `Box4x1Shape`, `Box2x2Shape`, `Box2x3Shape`, `Box3x2Shape`, `Box2x4Shape`, `Box4x2Shape`, `Box3x3Shape`, `Box3x4Shape`, `Box4x3Shape`, `Box4x4Shape`.
- **Morphology:** `OrthogonalTetromino`, `DiagonalPolyplet`.
- **Landing Cavities:** `FlatLandingShape` (`0` holes), `SingleCavityShape` (`1` hole), `MultiCavityShape` (`>=2` holes).
- `classify_extetromino(coords, piece_id=None, name=None) -> ExTetromino`: instantiates the matching cached composite `(Box, Morphology, Cavity)` subclass; composite instances support `.reclassify()` and `.clone()`.

### `class ExTetrominoFactory(grid_size=4)`
- `all_fixed() -> list[ExTetromino]`: all **110** unique oriented 4-polyplets.
- `all_one_sided() -> list[ExTetromino]`: **34** rotation-canonical 4-polyplets.
- `all_free() -> list[ExTetromino]`: **22** dihedral-canonical 4-polyplets.
- `classic_one_sided()` (**7**), `classic_fixed()` (**19**), `extended_one_sided()` (**27**), `extended_fixed()` (**91**).
- `by_id(piece_id: int) -> ExTetromino`, `filter(predicate) -> list[ExTetromino]`, `summary() -> dict`.

---

## 2. Board (`extetris.board`)

### `class Board(width=10, height=20)`
- `is_valid_position(shape, offset) -> bool` / `collision(shape, offset) -> bool`
- `get_ghost_row(shape, cursor) -> int`: lowest valid landing row below `cursor`.
- `insertShape(shape, rowIndex=0, columnIndex=0)` / `removeShape(shape, rowIndex=0, columnIndex=0)`
- `clear_full_lines() -> int`: clears completed rows and shifts upper rows down.
- `column_heights() -> list[int]`, `get_max_height() -> int`, `count_holes() -> int`, `get_bumpiness() -> int`, `clone() -> Board`.

---

## 3. Functional-OO Distributions (`extetris.distributions`)

### `class ShapeDistribution(seed=None)` *(ABC)*
- `sample(board=None, history=None) -> ExTetromino`
- `sample_many(count, board=None, history=None) -> list[ExTetromino]`
- **Combinators:** `.filter(predicate, seed=None)`, `.map(transform_fn, seed=None)`, `.blend(other, weight=0.5, seed=None)`, `.conditional(predicate_fn, other_true, other_false=None, seed=None)`, `dist1 + dist2`, `dist >> fn`.

### Concrete Strategies
- `UniformDistribution(shapes, seed=None)`
- `WeightedDistribution(shapes_or_mapping, weights=None, seed=None)`
- `BagDistribution(shapes, bag_multiplier=1, seed=None)`
- `AdaptiveDifficultyDistribution(shapes, seed=None)` (`.compute_distress(board)`, `.weights_for_board(board)`)
- `MarkovDistribution(shapes, transition_matrix=None, repeat_penalty=0.1, seed=None)`

---

## 4. Engine, FSM & Persistence (`extetris.engine`)

### `class GameState(Enum)`
`READY`, `RUNNING`, `PAUSED`, `GAME_OVER`.

### `class ExTetrisEngine(width=10, height=20, distribution=None, initial_speed_ms=1000, speed_factor=0.92, enable_wall_kicks=True, enable_ghost=True)`
- **FSM Controls:** `start()`, `pause()`, `resume()`, `toggle_pause()`, `new_game(auto_start=True)`
- **Actions:** `move_left()`, `move_right()`, `rotate_cw()`, `rotate_ccw()`, `soft_drop()` (`+1` pt), `hard_drop()` (`+2` pts/cell), `step()`, `speed_up()`, `slow_down()`
- **Observers:** `register_callback(event_or_fn, callback=None)` — emits `state_changed`, `piece_spawned`, `piece_moved`, `piece_rotated`, `piece_locked`, `lines_cleared`, `level_up`, `speed_changed`, `game_over`, `render_needed` (subscribe to `"*"` for all events).
- **Display & Telemetry:** `get_ghost_cursor()`, `get_render_composite()` (`0=empty`, `1=locked`, `2=ghost`, `3=active`), `is_paused`, `is_game_over`.
- **Persistence:** `save_state(path)`, `ExTetrisEngine.load_state(path, distribution=None)`, `export_text_board(path)`.

---

## 5. Renderers (`extetris.renderers`)
- `AbstractRenderer`: `.attach(engine)`, `.render(engine)`, `.run(engine, **kwargs)`, `.close()`.
- `HeadlessRenderer(capture_composites=True)`: captures `.frames`, `.composites`, `.snapshots`; `.run(engine, steps=20, action_sequence=None)`.
- `CLIRenderer(stream=None, use_ansi=True, tick_sleep=0.02)`: non-blocking terminal UI (`termios`/`select` or `msvcrt`).
- `TkinterRenderer(title="ExTetris Engine")`: lazy Tk UI with `TkinterRenderer.is_available()`.
- `create_renderer(name="cli", **kwargs)`

---

## 6. Configuration & Fluent Builder (`extetris.config`, `extetris.builder`, `extetris.cli`)
- `load_config(path)`, `save_config(config_data, path)`, `validate_config(raw_config)`, `get_default_config()`, `ConfigValidationError`.
- `ExTetrisBuilder(initial_config=None)`:
  - `ExTetrisBuilder.from_json(path)`, `.load_json(path)`
  - `.with_name(name, description=None)`, `.use_classic_tetris()`, `.use_extended_tetris(piece_scope="one_sided")`, `.use_chaos_tetris()`
  - `.filter_max_holes(max_holes)`, `.filter_orthogonal_only()`, `.filter_diagonal_only()`, `.filter_by(predicate)`
  - `.with_board_size(width, height)`, `.with_speed(initial_speed_ms, speed_factor=0.92)`, `.with_wall_kicks(enabled=True)`, `.with_ghost(enabled=True)`
  - `.with_distribution(strategy_or_dist, seed=None, bag_multiplier=1, repeat_penalty=0.1, weights_by_id=None)`
  - `.with_renderer(renderer_name)`, `.validate()`, `.build() -> (ExTetrisEngine, AbstractRenderer)`, `.export_variant(output_dir) -> dict`
- `load_game_from_json(path) -> (ExTetrisEngine, AbstractRenderer)`
- `extetris.cli.main(argv=None)` (console command `extetris`).
