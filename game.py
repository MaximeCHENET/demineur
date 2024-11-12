import tkinter as tk
from tkinter import messagebox
import time
from models.game_board import GameBoard
from models.score_manager import ScoreManager
from models.seed_manager import SeedManager
from ui.menu_ui import MenuUI
from ui.game_ui import GameUI
from ui.score_dialog import ScoreDialog, ScoresWindow
from ui.replay_dialog import ReplayDialog

class MinesweeperGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Des mineurs")
        self.root.geometry("1000x800")

        self.score_manager = ScoreManager()
        self.seed_manager = SeedManager()
        self.game_board = None
        self.game_ui = None
        self.menu_ui = None
        self.start_time = None
        self.timer_id = None

        self.show_menu()

    def show_menu(self):
        if self.game_ui:
            self.game_ui.destroy()

        self.menu_ui = MenuUI(self.root, self.start_game, self.show_high_scores, self.show_replay_dialog)

    def show_replay_dialog(self):
        recent_seeds = self.seed_manager.get_recent_seeds()
        if not recent_seeds:
            messagebox.showinfo("Replay", "Aucune partie précédente disponible!")
            return
        ReplayDialog(self.root, recent_seeds, self.start_game_with_seed)

    def start_game_with_seed(self, height, width, mines, seed):
        """Launch a game replay with a specific seed."""
        self.start_game(height, width, mines, seed)

    def show_replay_dialog(self):
        recent_seeds = self.seed_manager.get_recent_seeds()
        if not recent_seeds:
            messagebox.showinfo("Replay", "Aucune partie précédente disponible!")
            return

        ReplayDialog(self.root, recent_seeds, self.start_game_with_seed)

    def start_game_with_seed(self, seed_data):
        self.start_game(
            seed_data['height'],
            seed_data['width'],
            seed_data['mines'],
            seed_data['seed'],
            seed_data['first_click']
        )

    def on_cell_click(self, x, y):
        if not self.game_board.game_started:
            self.game_board.place_mines(x, y)
            self.seed_manager.save_seed(
                self.game_board.get_seed(),
                self.game_board.width,
                self.game_board.height,
                self.game_board.mines,
                (x, y)
            )

        cell = self.game_board.cells[x][y]
        if cell.is_flagged or cell.is_revealed:
            return

        if cell.is_mine:
            self.game_over()
        else:
            revealed_cells = self.game_board.reveal_cell(x, y)
            for rx, ry in revealed_cells:
                self.game_ui.update_cell(rx, ry)

            if self.game_board.check_win():
                self.win_game()

    def on_right_click(self, x, y):
        cell = self.game_board.cells[x][y]
        if cell.toggle_flag():
            self.game_ui.update_cell(x, y)
            if self.game_board.check_win():
                self.win_game()

    def start_timer(self):
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        if self.start_time is not None:
            elapsed_time = int(time.time() - self.start_time)
            self.game_ui.update_timer(elapsed_time)
            self.timer_id = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def start_game(self, height, width, mines, seed=None, first_click=None):
        """Start a game with specific dimensions, mines, seed, and first_click."""

        try:
            if height <= 0 or width <= 0 or mines <= 0:
                raise ValueError("Les valeurs doivent être positives")
            if mines >= height * width:
                raise ValueError("Trop de mines pour la taille du terrain")

            if self.menu_ui:
                self.menu_ui.destroy()

            self.game_board = GameBoard(height, width, mines, seed, first_click)

            self.game_ui = GameUI(self.root, self.game_board,
                                self.on_cell_click, self.on_right_click,
                                self.return_to_menu)

            self.start_timer()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def game_over(self):
        self.stop_timer()
        self.game_ui.show_mines()
        messagebox.showinfo("Game Over", "Vous avez perdu!")
        self.return_to_menu()

    def win_game(self):
        self.stop_timer()
        elapsed_time = int(time.time() - self.start_time)

        def save_score(player_name):
            self.score_manager.save_score(
                player_name,
                elapsed_time,
                self.game_board.width,
                self.game_board.height,
                self.game_board.mines
            )
            self.return_to_menu()

        ScoreDialog(self.root, elapsed_time, save_score)

    def show_high_scores(self):
        scores = self.score_manager.get_high_scores()
        if not scores:
            messagebox.showinfo("Scores", "Aucun score enregistré!")
            return
        ScoresWindow(self.root, scores)

    def return_to_menu(self):
        self.stop_timer()
        self.show_menu()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()
