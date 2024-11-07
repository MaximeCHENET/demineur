import tkinter as tk
from tkinter import ttk


class ScoreDialog:
    """Dialog for saving player's score after winning."""

    def __init__(self, root, elapsed_time, on_save):
        """Initialize the score dialog.

        Args:
            root: Tkinter root window
            elapsed_time (int): Time taken to complete the game
            on_save: Callback for saving the score
        """
        self.dialog = tk.Toplevel(root)
        self.dialog.title("Victoire!")
        self.dialog.geometry("300x150")
        self.dialog.transient(root)
        self.dialog.grab_set()

        # Victory message
        ttk.Label(self.dialog,
                  text=f"Félicitations! Vous avez gagné en {elapsed_time} secondes!").pack(pady=10)
        ttk.Label(self.dialog, text="Entrez votre nom:").pack()

        # Name input
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(self.dialog, textvariable=self.name_var)
        name_entry.pack(pady=10)

        # Save button
        ttk.Button(self.dialog, text="Enregistrer",
                   command=lambda: self._save_and_close(on_save)).pack(pady=10)

        name_entry.focus_set()

    def _save_and_close(self, on_save):
        """Save the score and close the dialog.

        Args:
            on_save: Callback function to save the score
        """
        player_name = self.name_var.get().strip()
        if player_name:
            on_save(player_name)
            self.dialog.destroy()


class ScoresWindow:
    """Window for displaying high scores."""

    def __init__(self, root, scores):
        """Initialize the scores window.

        Args:
            root: Tkinter root window
            scores (list): List of score dictionaries
        """
        self.window = tk.Toplevel(root)
        self.window.title("Meilleurs scores")
        self.window.geometry("400x300")

        # Create text widget for scores
        text_widget = tk.Text(self.window, wrap=tk.WORD, width=50, height=15)
        text_widget.pack(padx=10, pady=10)

        # Display scores
        text_widget.insert(tk.END, "MEILLEURS SCORES\n\n")
        for i, score in enumerate(scores, 1):
            text_widget.insert(tk.END,
                               f"{i}. {score['name']} - {score['time']}s\n"
                               f"   Grille: {score['width']}x{score['height']}, Mines: {score['mines']}\n"
                               f"   Date: {score['date']}\n\n"
                               )

        text_widget.config(state=tk.DISABLED)