import tkinter as tk
from tkinter import ttk


class MenuUI:
    """Manages the main menu user interface."""

    def __init__(self, root, on_start_game, on_show_scores):
        """Initialize the menu UI.

        Args:
            root: Tkinter root window
            on_start_game: Callback for starting a new game
            on_show_scores: Callback for showing high scores
        """
        self.root = root
        self.on_start_game = on_start_game
        self.on_show_scores = on_show_scores
        self.frame = None
        self.height_var = tk.StringVar(value="10")
        self.width_var = tk.StringVar(value="10")
        self.mines_var = tk.StringVar(value="15")
        self.create_menu()

    def create_menu(self):
        """Create the main menu UI elements."""
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(self.frame, text="Démineur", font=('Arial', 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Game settings inputs
        ttk.Label(self.frame, text="Hauteur:").grid(row=1, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.height_var).grid(row=1, column=1, pady=5)

        ttk.Label(self.frame, text="Largeur:").grid(row=2, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.width_var).grid(row=2, column=1, pady=5)

        ttk.Label(self.frame, text="Nombre de mines:").grid(row=3, column=0, pady=5)
        ttk.Entry(self.frame, textvariable=self.mines_var).grid(row=3, column=1, pady=5)

        # Action buttons
        start_button = ttk.Button(self.frame, text="Nouvelle Partie",
                                  command=lambda: self.on_start_game(
                                      int(self.height_var.get()),
                                      int(self.width_var.get()),
                                      int(self.mines_var.get())
                                  ))
        start_button.grid(row=4, column=0, columnspan=2, pady=10)

        scores_button = ttk.Button(self.frame, text="Voir les scores",
                                   command=self.on_show_scores)
        scores_button.grid(row=5, column=0, columnspan=2, pady=10)

    def destroy(self):
        """Clean up the UI elements."""
        if self.frame:
            self.frame.destroy()