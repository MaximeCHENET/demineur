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

    DIFFICULTY_PRESETS = {
        "Facile": {"width": 10, "height": 10, "mines": 10},
        "Moyen": {"width": 16, "height": 16, "mines": 40},
        "Difficile": {"width": 16, "height": 30, "mines": 99}
    }

    def __init__(self, root, scores, on_replay=None):
        """Initialize the scores window.

        Args:
            root: Tkinter root window
            scores (list): List of score dictionaries
            on_replay: Callback for replaying a game configuration
        """
        self.window = tk.Toplevel(root)
        self.window.title("Meilleurs scores")
        self.window.geometry("600x500")
        self.on_replay = on_replay

        # Create notebook for different difficulty tabs
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs for each difficulty
        self.create_difficulty_tab(notebook, "Facile", scores)
        self.create_difficulty_tab(notebook, "Moyen", scores)
        self.create_difficulty_tab(notebook, "Difficile", scores)
        self.create_difficulty_tab(notebook, "Personnalisé", scores)

    def close(self):
        """Close the scores window."""
        self.window.destroy()

    def create_difficulty_tab(self, notebook, difficulty, scores):
        """Create a tab for a specific difficulty level.

        Args:
            notebook: Notebook widget
            difficulty (str): Difficulty level
            scores (list): List of all scores
        """
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=difficulty)

        # Create scrollable frame
        canvas = tk.Canvas(tab)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Filter scores for this difficulty
        difficulty_scores = self.filter_scores_by_difficulty(scores, difficulty)

        if not difficulty_scores:
            ttk.Label(scrollable_frame, text="Aucun score pour cette difficulté").pack(pady=10)
        else:
            for i, score in enumerate(difficulty_scores, 1):
                self.create_score_frame(scrollable_frame, i, score)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_score_frame(self, parent, rank, score):
        """Create a frame for displaying a single score.

        Args:
            parent: Parent widget
            rank (int): Score rank
            score (dict): Score data
        """
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=5, pady=5)

        # Score information
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.X)

        ttk.Label(info_frame,
                  text=f"#{rank} - {score['name']}",
                  font=('TkDefaultFont', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame,
                  text=f"Temps: {score['time']}s").pack(side=tk.LEFT, padx=5)
        ttk.Label(info_frame,
                  text=f"Grille: {score['width']}x{score['height']}, Mines: {score['mines']}").pack(side=tk.LEFT,
                                                                                                    padx=5)

        # Add the seed if it exists
        if 'seed' in score:
            ttk.Label(info_frame,
                      text=f"Seed: {score['seed']}").pack(side=tk.LEFT, padx=5)

        if self.on_replay and 'seed' in score and 'first_click' in score:
            ttk.Button(info_frame,
                       text="Rejouer",
                       command=lambda: self._handle_replay(
                           score['height'],
                           score['width'],
                           score['mines'],
                           score['seed'],
                           score['first_click']
                       )).pack(side=tk.RIGHT, padx=5)

        ttk.Separator(frame, orient='horizontal').pack(fill=tk.X, pady=5)

    def _handle_replay(self, height, width, mines, seed, first_click):
        """Handle replay button click.

        Closes the scores window and calls the replay callback.

        Args:
            height (int): Board height
            width (int): Board width
            mines (int): Number of mines
            seed (int): Game seed
            first_click (tuple): First click coordinates
        """
        self.close()  # Close the scores window
        if self.on_replay:
            self.on_replay(height, width, mines, seed, first_click)

    def filter_scores_by_difficulty(self, scores, difficulty):
        """Filter scores to show only those matching the selected difficulty.

        Args:
            scores (list): List of all score records
            difficulty (str): Selected difficulty level

        Returns:
            list: Filtered list of scores matching the difficulty criteria
        """
        if difficulty == "Personnalisé":
            return [s for s in scores if not any(
                s['width'] == preset['width'] and
                s['height'] == preset['height'] and
                s['mines'] == preset['mines']
                for preset in self.DIFFICULTY_PRESETS.values()
            )]

        preset = self.DIFFICULTY_PRESETS.get(difficulty)
        if preset:
            return [s for s in scores if
                    s['width'] == preset['width'] and
                    s['height'] == preset['height'] and
                    s['mines'] == preset['mines']]

        return []