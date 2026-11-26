# engine.py: UI-agnostic 4-state FSM ExTetrisEngine with Observer callbacks (Attempt 3)
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from enum import Enum
import math
import numpy

from board import Board
from distributions import BagDistribution, ShapeDistribution
from factory import ExTetrominoFactory


class GameState(Enum):
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"


class ExTetrisEngine(object):
    """
    UI-agnostic Extended Tetris game engine governed by a 4-state FSM
    (READY -> RUNNING <-> PAUSED -> GAME_OVER) with Observer callbacks,
    wall-kick recovery, ghost projection, and level/speed progression.
    """

    WALL_KICK_OFFSETS = ((0, 0), (0, -1), (0, 1), (0, -2), (0, 2))
    LINE_CLEAR_POINTS = {1: 100, 2: 300, 3: 500, 4: 800}

    def __init__(
        self,
        width=10,
        height=20,
        distribution=None,
        initial_speed_ms=1000,
        speed_factor=0.92,
        enable_wall_kicks=True,
        enable_ghost=True,
    ):
        self.width = int(width)
        self.height = int(height)
        self.board = Board(width=self.width, height=self.height)
        self.factory = ExTetrominoFactory()
        if distribution is None:
            distribution = BagDistribution(self.factory.classic_one_sided())
        if not isinstance(distribution, ShapeDistribution):
            raise TypeError("distribution must be an instance of ShapeDistribution.")
        self.distribution = distribution

        self.initial_speed_ms = int(initial_speed_ms)
        if self.initial_speed_ms < 100:
            raise ValueError("initial_speed_ms must be >= 100.")
        self.speed_factor = float(speed_factor)
        self.drop_speed_ms = self.initial_speed_ms
        self.enable_wall_kicks = bool(enable_wall_kicks)
        self.enable_ghost = bool(enable_ghost)

        self.state = GameState.READY
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.history = []

        self._callbacks = {}
        self.current_piece = None
        self.next_piece = None
        self.cursor = (0, 0)
        self._init_pieces()

    # -----------------------------------------------------------------------
    # Properties & Observer Pattern
    # -----------------------------------------------------------------------
    @property
    def is_paused(self):
        return self.state == GameState.PAUSED

    @property
    def is_game_over(self):
        return self.state == GameState.GAME_OVER

    def register_callback(self, event_or_fn, callback=None):
        """
        Register an observer callback.
        Usage:
          engine.register_callback("lines_cleared", fn)
          engine.register_callback(fn)  # subscribes to all events ("*")
        """
        if callable(event_or_fn) and callback is None:
            event_name = "*"
            fn = event_or_fn
        else:
            event_name = str(event_or_fn)
            fn = callback
        if not callable(fn):
            raise TypeError("Observer callback must be callable.")
        self._callbacks.setdefault(event_name, []).append(fn)

    def _emit(self, event_name, **payload):
        payload.setdefault("event", event_name)
        payload.setdefault("state", self.state)
        for fn in self._callbacks.get(event_name, []):
            fn(payload)
        for fn in self._callbacks.get("*", []):
            fn(payload)

    def _transition_to(self, new_state):
        old_state = self.state
        if old_state == new_state:
            return False
        self.state = new_state
        self._emit("state_changed", old_state=old_state, new_state=new_state)
        return True

    # -----------------------------------------------------------------------
    # FSM Lifecycle Controls
    # -----------------------------------------------------------------------
    def _spawn_cursor(self, piece):
        col = max(0, (self.width - piece.width) // 2)
        return (0, col)

    def _init_pieces(self):
        self.current_piece = self.distribution.sample(board=self.board, history=self.history)
        self.history.append(self.current_piece)
        self.next_piece = self.distribution.sample(board=self.board, history=self.history)
        self.history.append(self.next_piece)
        self.cursor = self._spawn_cursor(self.current_piece)

    def start(self):
        """Transition READY -> RUNNING."""
        if self.state != GameState.READY:
            return False
        self._transition_to(GameState.RUNNING)
        self._emit("render_needed")
        return True

    def pause(self):
        """Transition RUNNING -> PAUSED."""
        if self.state != GameState.RUNNING:
            return False
        self._transition_to(GameState.PAUSED)
        self._emit("render_needed")
        return True

    def resume(self):
        """Transition PAUSED -> RUNNING."""
        if self.state != GameState.PAUSED:
            return False
        self._transition_to(GameState.RUNNING)
        self._emit("render_needed")
        return True

    def toggle_pause(self):
        if self.state == GameState.RUNNING:
            return self.pause()
        if self.state == GameState.PAUSED:
            return self.resume()
        return False

    def new_game(self, auto_start=True):
        """Reset board, score, level, and pieces; optionally enter RUNNING immediately."""
        self.board = Board(width=self.width, height=self.height)
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.drop_speed_ms = self.initial_speed_ms
        self.history = []
        self._init_pieces()
        target = GameState.RUNNING if auto_start else GameState.READY
        if self.state != target:
            self._transition_to(target)
        else:
            self._emit("state_changed", old_state=self.state, new_state=target)
        self._emit(
            "piece_spawned",
            piece=self.current_piece,
            next_piece=self.next_piece,
            cursor=self.cursor,
        )
        self._emit("render_needed")
        return True

    # -----------------------------------------------------------------------
    # Piece Movement, Wall-Kick Rotation & Gravity
    # -----------------------------------------------------------------------
    def _ensure_running(self):
        return self.state == GameState.RUNNING

    def move_left(self):
        return self._move_by(0, -1, "LEFT")

    def move_right(self):
        return self._move_by(0, 1, "RIGHT")

    def _move_by(self, dr, dc, label):
        if not self._ensure_running():
            return False
        new_cursor = (self.cursor[0] + dr, self.cursor[1] + dc)
        if not self.board.is_valid_position(self.current_piece, new_cursor):
            return False
        self.cursor = new_cursor
        self._emit("piece_moved", direction=label, cursor=self.cursor)
        self._emit("render_needed")
        return True

    def rotate_cw(self):
        return self._rotate("CW")

    def rotate_ccw(self):
        return self._rotate("CCW")

    def _rotate(self, direction):
        if not self._ensure_running():
            return False
        rotated = self.current_piece.clone()
        if direction == "CW":
            rotated.rotateCW()
        else:
            rotated.rotateAntiCW()
        if hasattr(rotated, "reclassify"):
            rotated = rotated.reclassify()

        kicks = self.WALL_KICK_OFFSETS if self.enable_wall_kicks else ((0, 0),)
        for dr, dc in kicks:
            candidate = (self.cursor[0] + dr, self.cursor[1] + dc)
            if self.board.is_valid_position(rotated, candidate):
                self.current_piece = rotated
                self.cursor = candidate
                self._emit(
                    "piece_rotated",
                    direction=direction,
                    kick_offset=(dr, dc),
                    piece=self.current_piece,
                    cursor=self.cursor,
                )
                self._emit("render_needed")
                return True
        return False

    def soft_drop(self):
        """Move piece down 1 cell (+1 score) or lock if blocked."""
        if not self._ensure_running():
            return False
        if self._move_by(1, 0, "DOWN"):
            self.score += 1
            return True
        self._lock_and_advance()
        return False

    def hard_drop(self):
        """Drop piece straight to ghost row (+2 score per cell) and lock."""
        if not self._ensure_running():
            return 0
        ghost_r = self.board.get_ghost_row(self.current_piece, self.cursor)
        distance = max(0, ghost_r - self.cursor[0])
        self.cursor = (ghost_r, self.cursor[1])
        self.score += 2 * distance
        self._lock_and_advance()
        return distance

    def step(self):
        """Advance one gravity tick without soft-drop points."""
        if not self._ensure_running():
            return False
        if self._move_by(1, 0, "GRAVITY"):
            return True
        self._lock_and_advance()
        return False

    def _recompute_level_and_speed(self):
        old_level = self.level
        tiers = self.lines_cleared // 10
        self.level = 1 + tiers
        self.drop_speed_ms = max(100, int(round(self.initial_speed_ms * (self.speed_factor ** tiers), 6)))
        if self.level != old_level:
            self._emit("level_up", old_level=old_level, new_level=self.level, drop_speed_ms=self.drop_speed_ms)
            self._emit("speed_changed", drop_speed_ms=self.drop_speed_ms)

    def speed_up(self):
        self.drop_speed_ms = max(100, int(math.floor(round(self.drop_speed_ms * 0.9, 6))))
        self._emit("speed_changed", drop_speed_ms=self.drop_speed_ms)

    def slow_down(self):
        self.drop_speed_ms = int(math.ceil(round(self.drop_speed_ms * 1.1, 6)))
        self._emit("speed_changed", drop_speed_ms=self.drop_speed_ms)

    def _lock_and_advance(self):
        self.board.insertShape(self.current_piece, self.cursor[0], self.cursor[1])
        self._emit(
            "piece_locked",
            piece=self.current_piece,
            cursor=self.cursor,
            board_holes=self.board.count_holes(),
            max_height=self.board.get_max_height(),
        )

        cleared = self.board.clear_full_lines()
        if cleared > 0:
            self.lines_cleared += cleared
            base_pts = self.LINE_CLEAR_POINTS.get(cleared, 200 * cleared)
            self.score += base_pts * self.level
            self._recompute_level_and_speed()
            self._emit(
                "lines_cleared",
                lines=cleared,
                total_lines=self.lines_cleared,
                score=self.score,
                level=self.level,
            )

        self.current_piece = self.next_piece
        self.cursor = self._spawn_cursor(self.current_piece)
        self.next_piece = self.distribution.sample(board=self.board, history=self.history)
        self.history.append(self.next_piece)

        if not self.board.is_valid_position(self.current_piece, self.cursor):
            self._transition_to(GameState.GAME_OVER)
            self._emit(
                "game_over",
                score=self.score,
                lines_cleared=self.lines_cleared,
                level=self.level,
            )
        else:
            self._emit(
                "piece_spawned",
                piece=self.current_piece,
                next_piece=self.next_piece,
                cursor=self.cursor,
            )
        self._emit("render_needed")

    # -----------------------------------------------------------------------
    # Persistence (JSON Save/Load/Resume + Text Board Export)
    # -----------------------------------------------------------------------
    def save_state(self, path):
        from persistence import save_engine_state
        return save_engine_state(self, path)

    @classmethod
    def load_state(cls, path, distribution=None):
        from persistence import load_engine_state
        return load_engine_state(path, cls, GameState, custom_distribution=distribution)

    def export_text_board(self, path):
        from persistence import export_text_board
        return export_text_board(self, path)

    # -----------------------------------------------------------------------
    # Ghost Projection & Composite Render Snapshot
    # -----------------------------------------------------------------------
    def get_ghost_cursor(self):
        if self.current_piece is None:
            return self.cursor
        ghost_r = self.board.get_ghost_row(self.current_piece, self.cursor)
        return (ghost_r, self.cursor[1])

    def get_render_composite(self):
        """
        Return 2D integer matrix combining:
          0 = empty cell
          1 = locked board block
          2 = ghost landing projection
          3 = active falling piece
        """
        comp = self.board.area.astype(int)
        if self.current_piece is not None:
            if self.enable_ghost and self.state != GameState.GAME_OVER:
                gr, gc = self.get_ghost_cursor()
                for dr, dc in self.current_piece.coords:
                    r, c = gr + dr, gc + dc
                    if 0 <= r < self.height and 0 <= c < self.width and comp[r, c] == 0:
                        comp[r, c] = 2
            cr, cc = self.cursor
            for dr, dc in self.current_piece.coords:
                r, c = cr + dr, cc + dc
                if 0 <= r < self.height and 0 <= c < self.width:
                    comp[r, c] = 3
        return comp
