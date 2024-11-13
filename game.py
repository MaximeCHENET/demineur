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
        """Display the main menu."""
        if self.game_ui:
            self.game_ui.destroy()

        self.menu_ui = MenuUI(self.root, self.start_game, self.show_high_scores, self.show_replay_dialog)

    def show_replay_dialog(self):
        """Show the replay dialog with recent games."""
        recent_seeds = self.seed_manager.get_recent_seeds()
        if not recent_seeds:
            messagebox.showinfo("Replay", "Aucune partie précédente disponible!")
            return
        ReplayDialog(self.root, recent_seeds, self.start_game_with_seed_data)

    def start_game_with_seed_data(self, seed_data):
        """Start a game with seed data from replay dialog.

        Args:
            seed_data (dict): Dictionary containing game configuration
        """
        self.start_game_with_seed(
            seed_data['height'],
            seed_data['width'],
            seed_data['mines'],
            seed_data['seed'],
            seed_data['first_click']
        )

    def start_game_with_seed(self, height, width, mines, seed, first_click):
        """Start a game with specific parameters.

        Args:
            height (int): Board height
            width (int): Board width
            mines (int): Number of mines
            seed (int): Random seed
            first_click (tuple): First click coordinates
        """
        if self.menu_ui:
            self.menu_ui.destroy()

        self.game_board = GameBoard(height, width, mines, seed, first_click)

        self.game_ui = GameUI(self.root, self.game_board,
                              self.on_cell_click, self.on_right_click,
                              self.return_to_menu)

        self.start_timer()

    def on_cell_click(self, x, y):
        """Handle left click on a cell.

        Args:
            x (int): Cell x coordinate
            y (int): Cell y coordinate
        """
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
        """Handle right click on a cell.

        Args:
            x (int): Cell x coordinate
            y (int): Cell y coordinate
        """
        cell = self.game_board.cells[x][y]
        if cell.toggle_flag():
            self.game_ui.update_cell(x, y)
            if self.game_board.check_win():
                self.win_game()

    def start_timer(self):
        """Start the game timer."""
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """Update the timer display."""
        if self.start_time is not None:
            elapsed_time = int(time.time() - self.start_time)
            self.game_ui.update_timer(elapsed_time)
            self.timer_id = self.root.after(1000, self.update_timer)

    def stop_timer(self):
        """Stop the game timer."""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def start_game(self, height, width, mines, seed=None, first_click=None):
        """Start a new game with given parameters.

        Args:
            height (int): Board height
            width (int): Board width
            mines (int): Number of mines
            seed (int, optional): Random seed
            first_click (tuple, optional): First click coordinates
        """
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
        """Handle game over state."""
        self.stop_timer()
        self.game_ui.show_mines()
        messagebox.showinfo("Game Over", "Vous avez perdu!")
        self.return_to_menu()

    def win_game(self):
        """Handle game win state."""
        self.stop_timer()
        elapsed_time = int(time.time() - self.start_time)

        def save_score(player_name):
            self.score_manager.save_score(
                player_name,
                elapsed_time,
                self.game_board.width,
                self.game_board.height,
                self.game_board.mines,
                self.game_board.get_seed(),
                self.game_board.first_click_position
            )
            self.return_to_menu()

        ScoreDialog(self.root, elapsed_time, save_score)

    def show_high_scores(self):
        """Display the high scores window."""
        scores = self.score_manager.get_high_scores()
        if not scores:
            messagebox.showinfo("Scores", "Aucun score enregistré!")
            return
        ScoresWindow(self.root, scores, on_replay=self.start_game_with_seed)

    def return_to_menu(self):
        """Return to the main menu."""
        self.stop_timer()
        self.show_menu()

    def run(self):
        """Start the game application."""
        self.root.mainloop()


if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()