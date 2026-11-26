# renderers.py: AbstractRenderer, HeadlessRenderer, CLIRenderer, and optional TkinterRenderer
# Copyright (C) 2026 ExTetris Contributors (GPL-3.0-or-later)

from abc import ABC, abstractmethod
import sys
import time

try:
    import termios
    import tty
    import select
    _HAS_POSIX_TTY = True
except ImportError:
    termios = None
    tty = None
    select = None
    _HAS_POSIX_TTY = False

try:
    import msvcrt
    _HAS_MSVCRT = True
except ImportError:
    msvcrt = None
    _HAS_MSVCRT = False


class AbstractRenderer(ABC):
    """Base interface decoupling ExTetrisEngine game logic from presentation."""

    def attach(self, engine):
        engine.register_callback("render_needed", lambda _payload: self.render(engine))
        return self

    @abstractmethod
    def render(self, engine):
        """Render the current engine state."""

    @abstractmethod
    def run(self, engine, **kwargs):
        """Run the interactive or scripted loop for the given engine."""

    def close(self):
        """Release any renderer resources."""


class HeadlessRenderer(AbstractRenderer):
    """Non-visual renderer capturing frames, composites, and state snapshots for automation/tests."""

    CELL_SYMBOLS = {0: ".", 1: "#", 2: ":", 3: "@"}

    def __init__(self, capture_composites=True):
        self.capture_composites = capture_composites
        self.frames = []
        self.composites = []
        self.snapshots = []

    def format_frame(self, engine):
        comp = engine.get_render_composite()
        lines = [
            f"State={engine.state.value} Score={engine.score} Lines={engine.lines_cleared} Level={engine.level}"
        ]
        border = "+" + "-" * (engine.width * 2) + "+"
        lines.append(border)
        for r in range(engine.height):
            row_cells = " ".join(self.CELL_SYMBOLS[int(comp[r, c])] for c in range(engine.width))
            lines.append(f"|{row_cells} |")
        lines.append(border)
        return "\n".join(lines)

    def render(self, engine):
        frame = self.format_frame(engine)
        self.frames.append(frame)
        if self.capture_composites:
            self.composites.append(engine.get_render_composite().copy())
        self.snapshots.append({
            "state": engine.state.value,
            "score": engine.score,
            "lines_cleared": engine.lines_cleared,
            "level": engine.level,
            "holes": engine.board.count_holes(),
            "max_height": engine.board.get_max_height(),
        })
        return frame

    def run(self, engine, steps=20, action_sequence=None):
        self.attach(engine)
        if engine.state.value == "READY":
            engine.start()
        else:
            self.render(engine)

        action_map = {
            "LEFT": engine.move_left,
            "RIGHT": engine.move_right,
            "CW": engine.rotate_cw,
            "CCW": engine.rotate_ccw,
            "SOFT_DROP": engine.soft_drop,
            "HARD_DROP": engine.hard_drop,
            "PAUSE": engine.pause,
            "RESUME": engine.resume,
            "STEP": engine.step,
        }

        actions = list(action_sequence) if action_sequence else []
        for step_idx in range(steps):
            if engine.is_game_over:
                break
            if step_idx < len(actions):
                act = actions[step_idx]
                fn = action_map.get(act)
                if fn is None:
                    raise ValueError(f"Unknown headless action: {act}")
                fn()
            else:
                engine.step()
        return self.frames


class NonBlockingKeyReader(object):
    """Cross-platform non-blocking keyboard reader (POSIX termios/select or Windows msvcrt)."""

    POSIX_ARROW_MAP = {
        "\x1b[A": "UP",
        "\x1b[B": "DOWN",
        "\x1b[C": "RIGHT",
        "\x1b[D": "LEFT",
    }

    def __init__(self, input_stream=None):
        self.input_stream = input_stream if input_stream is not None else sys.stdin
        self._fd = None
        self._old_settings = None
        self._is_tty = False

    def __enter__(self):
        if not _HAS_MSVCRT and _HAS_POSIX_TTY:
            try:
                if self.input_stream.isatty():
                    self._fd = self.input_stream.fileno()
                    self._old_settings = termios.tcgetattr(self._fd)
                    tty.setcbreak(self._fd)
                    self._is_tty = True
            except Exception:
                self._is_tty = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._is_tty and self._old_settings is not None and _HAS_POSIX_TTY:
            try:
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)
            except Exception:
                pass

    def poll_key(self):
        if _HAS_MSVCRT:
            if not msvcrt.kbhit():
                return None
            ch = msvcrt.getwch()
            if ch in ("\x00", "\xe0") and msvcrt.kbhit():
                ext = msvcrt.getwch()
                return {"H": "UP", "P": "DOWN", "M": "RIGHT", "K": "LEFT"}.get(ext)
            return ch

        if _HAS_POSIX_TTY and self._is_tty:
            ready, _, _ = select.select([self.input_stream], [], [], 0)
            if not ready:
                return None
            ch = self.input_stream.read(1)
            if ch == "\x1b":
                seq = ch
                for _ in range(2):
                    r2, _, _ = select.select([self.input_stream], [], [], 0.005)
                    if not r2:
                        break
                    seq += self.input_stream.read(1)
                return self.POSIX_ARROW_MAP.get(seq, seq)
            return ch
        return None


class CLIRenderer(AbstractRenderer):
    """ANSI terminal renderer with cross-platform non-blocking input."""

    ANSI_RESET = "\033[0m"
    ANSI_HOME_CLEAR = "\033[2J\033[H"
    ANSI_CELL = {
        0: "  ",
        1: "\033[36m[]\033[0m",
        2: "\033[90m::\033[0m",
        3: "\033[93m##\033[0m",
    }
    PLAIN_CELL = {0: " .", 1: "[]", 2: "::", 3: "##"}

    def __init__(self, stream=None, use_ansi=True, tick_sleep=0.02):
        self.stream = stream if stream is not None else sys.stdout
        self.use_ansi = bool(use_ansi)
        self.tick_sleep = float(tick_sleep)
        self.last_frame = ""

    def format_frame(self, engine):
        comp = engine.get_render_composite()
        cells = self.ANSI_CELL if self.use_ansi else self.PLAIN_CELL
        lines = []
        if self.use_ansi:
            lines.append(self.ANSI_HOME_CLEAR)
        header = (
            f"ExTetris | State: {engine.state.value} | Score: {engine.score} | "
            f"Lines: {engine.lines_cleared} | Level: {engine.level} | Speed: {engine.drop_speed_ms}ms"
        )
        lines.append(header)
        border = "+" + "--" * engine.width + "+"
        lines.append(border)
        for r in range(engine.height):
            row_str = "".join(cells[int(comp[r, c])] for c in range(engine.width))
            lines.append(f"|{row_str}|")
        lines.append(border)
        lines.append(
            f"Holes: {engine.board.count_holes()} | MaxH: {engine.board.get_max_height()} | "
            f"Bump: {engine.board.get_bumpiness()} | Next: {engine.next_piece.name if engine.next_piece else '-'}"
        )
        lines.append("Controls: [a/Left] [d/Right] [w/Up: CW] [e: CCW] [s/Down: Soft] [Space: Drop] [p: Pause] [q: Quit]")
        return "\n".join(lines) + "\n"

    def render(self, engine):
        frame = self.format_frame(engine)
        self.last_frame = frame
        self.stream.write(frame)
        self.stream.flush()
        return frame

    def handle_key(self, engine, key):
        if key is None:
            return True
        if key in ("q", "Q"):
            return False
        if key in ("p", "P"):
            engine.toggle_pause()
        elif key in ("LEFT", "a", "A"):
            engine.move_left()
        elif key in ("RIGHT", "d", "D"):
            engine.move_right()
        elif key in ("UP", "w", "W"):
            engine.rotate_cw()
        elif key in ("e", "E"):
            engine.rotate_ccw()
        elif key in ("DOWN", "s", "S"):
            engine.soft_drop()
        elif key == " ":
            engine.hard_drop()
        elif key in ("r", "R") and engine.is_game_over:
            engine.new_game()
        return True

    def run(self, engine, max_ticks=None):
        if engine.state.value == "READY":
            engine.start()
        self.render(engine)
        last_drop = time.monotonic()
        ticks = 0
        with NonBlockingKeyReader() as reader:
            while not engine.is_game_over:
                key = reader.poll_key()
                if not self.handle_key(engine, key):
                    break
                if key is not None:
                    self.render(engine)
                now = time.monotonic()
                if (now - last_drop) * 1000.0 >= engine.drop_speed_ms:
                    engine.step()
                    self.render(engine)
                    last_drop = now
                    ticks += 1
                    if max_ticks is not None and ticks >= max_ticks:
                        break
                time.sleep(self.tick_sleep)
        self.render(engine)
        return self.last_frame


class TkinterRenderer(AbstractRenderer):
    """Optional Tkinter GUI renderer that degrades cleanly when Tk/display is unavailable."""

    @staticmethod
    def is_available():
        try:
            import tkinter as tk
            probe = tk.Tk()
            probe.withdraw()
            probe.update_idletasks()
            probe.destroy()
            return True
        except Exception:
            return False

    def __init__(self, title="ExTetris Engine"):
        try:
            import tkinter as tk
            self._tk = tk
        except Exception as exc:
            raise RuntimeError("Tkinter is not available in this Python environment.") from exc
        self.title = title
        self.window = None
        self.text_area = None
        self.status_var = None
        self._engine = None

    def _ensure_window(self, engine):
        if self.window is not None:
            return
        tk = self._tk
        try:
            self.window = tk.Tk()
        except tk.TclError as exc:
            raise RuntimeError(f"Tkinter display unavailable: {exc}") from exc
        self.window.title(self.title)
        self.text_area = tk.Text(
            self.window,
            wrap=tk.NONE,
            height=engine.height,
            width=2 * engine.width,
            bg="#eceff4",
            fg="#1f2937",
            font=("Courier New", 16, "bold"),
        )
        self.text_area.pack(expand=tk.YES, fill=tk.BOTH)
        self.status_var = tk.StringVar(self.window, "")
        tk.Label(self.window, textvariable=self.status_var).pack()

        self.window.bind("<Left>", lambda _e: (engine.move_left(), self.render(engine)))
        self.window.bind("<Right>", lambda _e: (engine.move_right(), self.render(engine)))
        self.window.bind("<Up>", lambda _e: (engine.rotate_cw(), self.render(engine)))
        self.window.bind("<Down>", lambda _e: (engine.soft_drop(), self.render(engine)))
        self.window.bind("<space>", lambda _e: (engine.hard_drop(), self.render(engine)))
        self.window.bind("p", lambda _e: (engine.toggle_pause(), self.render(engine)))
        self.window.bind("e", lambda _e: (engine.rotate_ccw(), self.render(engine)))

    def format_frame(self, engine):
        comp = engine.get_render_composite()
        symbols = {0: "  ", 1: "\N{BLACK LARGE SQUARE}", 2: "::", 3: "\u25A3 "}
        return "\n".join(
            "".join(symbols[int(comp[r, c])] for c in range(engine.width))
            for r in range(engine.height)
        )

    def render(self, engine):
        if self.window is None:
            self._ensure_window(engine)
        tk = self._tk
        frame = self.format_frame(engine)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, frame)
        self.status_var.set(
            f"State: {engine.state.value} | Score: {engine.score} | Lines: {engine.lines_cleared} | Level: {engine.level}"
        )
        return frame

    def run(self, engine):
        self._engine = engine
        self._ensure_window(engine)
        self.attach(engine)
        if engine.state.value == "READY":
            engine.start()
        self.render(engine)

        def tick():
            if not engine.is_game_over:
                engine.step()
                self.render(engine)
                self.window.after(engine.drop_speed_ms, tick)

        self.window.after(engine.drop_speed_ms, tick)
        self.window.mainloop()

    def close(self):
        if self.window is not None:
            try:
                self.window.destroy()
            except Exception:
                pass
            self.window = None


def create_renderer(name="cli", **kwargs):
    key = name.strip().lower()
    if key == "headless":
        return HeadlessRenderer(**kwargs)
    if key == "cli":
        return CLIRenderer(**kwargs)
    if key in ("tk", "tkinter"):
        return TkinterRenderer(**kwargs)
    raise ValueError(f"Unknown renderer '{name}'. Expected one of: headless, cli, tk.")
