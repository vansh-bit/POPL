# engine.py: ExTetris engine wired to coordinate Shapes & ExTetrominoFactory (Attempt 2)
# Based on starter code Copyright (C) 2024 Ramprasad S. Joshi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random
import numpy
import tkinter as tk
from tkinter import filedialog, simpledialog
from board import Board
from factory import ExTetrominoFactory


class TetrisEngine:
    def __init__(self, piece_pool=None, factory=None, width=10, height=20, headless=False, seed=None):
        self.factory = factory or ExTetrominoFactory()
        self.piece_pool = list(piece_pool) if piece_pool is not None else self.factory.classic_one_sided()
        if not self.piece_pool:
            raise ValueError("piece_pool must contain at least one ExTetromino.")
        self._rng = random.Random(seed)
        self.headless = headless
        self.width = width
        self.height = height
        self.board = Board(width=self.width, height=self.height)
        self.pauseStatus = False
        self.update_duration = 100
        self.initial_move_down_duration = 1000
        self.move_down_duration = self.initial_move_down_duration
        self.default_cursor = (0, int(self.board.width / 2 - 1))
        self.cursor = self.default_cursor
        self.game_over_status = False
        self.deleted_lines = 0
        self.piece = None
        self.new_piece()

        self.window = None
        self.text_area = None
        self.score = None
        self.scoreboard = None

        if not self.headless:
            self.window = tk.Tk()
            self.window.title("Python Text Tetris (ExTetris Attempt 2)")
            self.text_area = tk.Text(
                self.window,
                wrap=tk.CHAR,
                height=self.height,
                width=2 * self.width,
                bg='light gray',
                fg='blue',
                font=('Courier New', '16', 'bold'),
            )
            self.text_area.pack(expand=tk.YES, fill=tk.BOTH)
            self.window.bind("<Up>", self.rotate_CW)
            self.window.bind("<Left>", self.move_left)
            self.window.bind("<Right>", self.move_right)
            self.window.bind("<space>", self.drop_piece)
            self.window.bind("<Down>", self.move_down_force)
            self.text_area.insert(tk.END, self.render())
            self.create_menu()
            self.score = tk.StringVar(self.window, "No. of Lines Cleared = " + str(self.deleted_lines))
            self.scoreboard = tk.Label(self.window, textvariable=self.score)
            self.scoreboard.pack()

    def run(self):
        if self.headless or self.window is None:
            raise RuntimeError("Cannot call run() in headless mode")
        self.window.after(self.update_duration, lambda: self.update_step())
        self.window.after(self.move_down_duration, lambda: self.move_down_step())
        self.window.mainloop()

    def render(self):
        area = self.board.clone()
        for dr, dc in self.piece.coords:
            r = self.cursor[0] + dr
            c = self.cursor[1] + dc
            if 0 <= r < self.height and 0 <= c < self.width:
                area.area[r, c] = True
        return str(area)

    def toggle_pause_status(self):
        self.pauseStatus = not self.pauseStatus

    def rotate_CW(self, event=None):
        if self.pauseStatus or self.game_over_status:
            return False
        newpiece = self.piece.clone()
        newpiece.rotateCW()
        if hasattr(newpiece, "reclassify"):
            newpiece = newpiece.reclassify()
        if self.board.collision(newpiece, self.cursor):
            return False
        self.piece = newpiece
        return True

    def rotate_AntiCW(self, event=None):
        if self.pauseStatus or self.game_over_status:
            return False
        newpiece = self.piece.clone()
        newpiece.rotateAntiCW()
        if hasattr(newpiece, "reclassify"):
            newpiece = newpiece.reclassify()
        if self.board.collision(newpiece, self.cursor):
            return False
        self.piece = newpiece
        return True

    def move_left(self, event=None):
        if self.pauseStatus or self.game_over_status:
            return False
        return self.move_piece('LEFT')

    def move_right(self, event=None):
        if self.pauseStatus or self.game_over_status:
            return False
        return self.move_piece('RIGHT')

    def drop_piece(self, event=None):
        if self.pauseStatus or self.game_over_status:
            return
        while self.move_piece('DOWN'):
            pass

    def move_down_force(self, event=None):
        self.move_down_step(True)

    def move_down_step(self, accelerated=False):
        if self.pauseStatus or self.game_over_status:
            if not accelerated and not self.headless and self.window is not None and not self.game_over_status:
                self.window.after(self.move_down_duration, lambda: self.move_down_step())
            return
        if not self.move_piece('DOWN'):
            self.board.insertShape(self.piece, self.cursor[0], self.cursor[1])
            cleared = self.board.clear_full_lines()
            if cleared:
                self.deleted_lines += cleared
                if self.score is not None:
                    self.score.set("No. of Lines Cleared = " + str(self.deleted_lines))
                if not (self.deleted_lines % 10):
                    self.speed_up()
            self.cursor = self.default_cursor
            self.new_piece()
            if self.board.collision(self.piece, self.cursor):
                self.game_over_status = True
                if not self.headless and self.window is not None:
                    string_board = self.render().split('\n')
                    string_board[int(self.height / 5)] = 'Game Over'
                    lastmessage = "\n".join(string_board[row].strip() for row in range(self.height)) + "\n"
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, lastmessage)
                    self.dialog = simpledialog.Dialog(self.window, "Game Over!")
                    self.window.quit()
        if not accelerated and not self.headless and self.window is not None and not self.game_over_status:
            self.window.after(self.move_down_duration, lambda: self.move_down_step())

    def update_step(self):
        if self.headless or self.window is None:
            return
        if self.pauseStatus:
            self.window.after(self.update_duration, lambda: self.update_step())
            return
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, self.render())
        self.window.after(self.update_duration, lambda: self.update_step())

    def speed_up(self):
        self.move_down_duration = max(50, int(numpy.floor(self.move_down_duration * 0.9)))

    def slow_down(self):
        self.move_down_duration = int(numpy.ceil(self.move_down_duration * 1.1))

    def extetricks_help(self):
        self.pauseStatus = True
        help_message = '''
        This is EXtendedTETRIckS (Attempt 2: Coordinate Shape Hierarchy).
        Copyright (C) 2024 Ramprasad S. Joshi.
        '''
        if not self.headless and self.text_area is not None:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, help_message)
            simpledialog.Dialog(self.window, "Click any button to continue")
        self.pauseStatus = False

    def create_menu(self):
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        extetris_menu = tk.Menu(menu)
        menu.add_cascade(label="EXtendedTETRIckS", menu=extetris_menu)
        extetris_menu.add_command(label="New Game", command=self.new_game)
        extetris_menu.add_separator()
        extetris_menu.add_command(label="Pause", command=self.toggle_pause_status)
        extetris_menu.add_separator()
        extetris_menu.add_command(label="Speed-Up", command=self.speed_up)
        extetris_menu.add_command(label="Slow-down", command=self.slow_down)
        extetris_menu.add_separator()
        extetris_menu.add_command(label="Save state", command=self.save_file)
        extetris_menu.add_separator()
        extetris_menu.add_command(label="Exit", command=self.window.quit)
        extetris_menu.add_separator()
        extetris_menu.add_command(label="About", command=self.extetricks_help)

    def new_piece(self, piece=None):
        if piece is None:
            self.piece = self._rng.choice(self.piece_pool).clone()
        else:
            self.piece = piece
        self.cursor = self.default_cursor

    def new_game(self):
        self.game_over_status = False
        self.pauseStatus = True
        self.board = Board(width=self.width, height=self.height)
        self.new_piece()
        if not self.headless and self.text_area is not None:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, self.render())
        self.cursor = self.default_cursor
        self.move_down_duration = self.initial_move_down_duration
        self.deleted_lines = 0
        if self.score is not None:
            self.score.set("No. of Lines Cleared = " + str(self.deleted_lines))
        self.pauseStatus = False

    def save_file(self):
        if self.headless or self.text_area is None:
            return
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file:
            with open(file, "w") as file_handler:
                file_handler.write(self.text_area.get(1.0, tk.END))
            self.window.title(f"Python Tetris Board - {file}")

    def move_piece(self, direction):
        offsets = {'LEFT': (0, -1), 'RIGHT': (0, 1), 'UP': (-1, 0), 'DOWN': (1, 0)}
        if direction not in offsets:
            raise ValueError(f"Unknown direction: {direction}")
        off_r, off_c = offsets[direction]
        new_cursor = (self.cursor[0] + off_r, self.cursor[1] + off_c)
        if self.board.collision(self.piece, new_cursor):
            return False
        self.cursor = new_cursor
        return True


if __name__ == "__main__":
    factory = ExTetrominoFactory()
    mode = input("Select mode [1=Classic (7), 2=One-Sided Extended (34), 3=All Fixed (110)]: ").strip()
    if mode == "2":
        pool = factory.all_one_sided()
    elif mode == "3":
        pool = factory.all_fixed()
    else:
        pool = factory.classic_one_sided()
    tetris_engine = TetrisEngine(piece_pool=pool)
    tetris_engine.run()
