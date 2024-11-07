# Main game controller class that orchestrates the game logic and UI components
import tkinter as tk
from tkinter import messagebox
import time
from models.game_board import GameBoard
from models.score_manager import ScoreManager
from ui.menu_ui import MenuUI
from ui.game_ui import GameUI
from ui.score_dialog import ScoreDialog, ScoresWindow


class MinesweeperGame:
    """Main game controller class that manages the game state and UI interactions."""

    def __init__(self):
        """Initialize the game window and core components."""
        self.root = tk.Tk()
        self.root.title("Démineur")
        self.root.geometry("800x600")

        # Initialize core components
        self.score_manager = ScoreManager()
        self.game_board = None
        self.game_ui = None
        self.menu_ui = None
        self.start_time = None
        self.timer_id = None

        self.show_menu()

    def show_menu(self):
        """Display the main menu screen."""
        if self.game_ui:
            self.game_ui.destroy()

        self.menu_ui = MenuUI(self.root, self.start_game, self.show_high_scores)

    def start_game(self, height, width, mines):
        """Start a new game with the specified dimensions and number of mines."""
        try:
            # Validate input parameters
            if height <= 0 or width <= 0 or mines <= 0:
                raise ValueError("Les valeurs doivent être positives")
            if mines >= height * width:
                raise ValueError("Trop de mines pour la taille du terrain")

            # Clean up existing UI and create new game
            if self.menu_ui:
                self.menu_ui.destroy()

            self.game_board = GameBoard(height, width, mines)
            self.game_ui = GameUI(self.root, self.game_board,
                                  self.on_cell_click, self.on_right_click,
                                  self.return_to_menu)

            messagebox.showinfo("Nouvelle partie", "La partie va commencer!")

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def on_cell_click(self, x, y):
        """Handle left-click events on cells."""
        # First click initializes the game
        if not self.game_board.game_started:
            self.game_board.place_mines(x, y)
            self.start_timer()

        cell = self.game_board.cells[x][y]
        if cell.is_flagged or cell.is_revealed:
            return

        if cell.is_mine:
            self.game_over()
        else:
            # Reveal clicked cell and update UI
            revealed_cells = self.game_board.reveal_cell(x, y)
            for rx, ry in revealed_cells:
                self.game_ui.update_cell(rx, ry)

            if self.game_board.check_win():
                self.win_game()

    def on_right_click(self, x, y):
        """Handle right-click events for flagging cells."""
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

    def game_over(self):
        """Handle game over state when a mine is clicked."""
        self.stop_timer()
        self.game_ui.show_mines()
        messagebox.showinfo("Game Over", "Vous avez perdu!")
        self.return_to_menu()

    def win_game(self):
        """Handle win state when all non-mine cells are revealed."""
        self.stop_timer()
        elapsed_time = int(time.time() - self.start_time)

        def save_score(player_name):
            """Save the player's score and return to menu."""
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
        """Display the high scores window."""
        scores = self.score_manager.get_high_scores()
        if not scores:
            messagebox.showinfo("Scores", "Aucun score enregistré!")
            return
        ScoresWindow(self.root, scores)

    def return_to_menu(self):
        """Return to the main menu."""
        self.stop_timer()
        self.show_menu()

    def run(self):
        """Start the game main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()