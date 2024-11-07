import tkinter as tk
from tkinter import ttk, messagebox


class MenuUI:
    """Main menu interface for the Minesweeper game."""

    DIFFICULTY_LEVELS = {
        "Facile": {"height": 10, "width": 10, "mines": 10},
        "Moyen": {"height": 16, "width": 16, "mines": 40},
        "Difficile": {"height": 16, "width": 30, "mines": 99}
    }

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
        self.custom_frame = None
        self.height_var = tk.StringVar(value="10")
        self.width_var = tk.StringVar(value="10")
        self.mines_var = tk.StringVar(value="10")
        self.difficulty_var = tk.StringVar(value="Facile")
        self.create_menu()

    def create_menu(self):
        """Create the main menu elements."""
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title = ttk.Label(self.frame, text="Démineur", font=('TkDefaultFont', 24, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # Difficulty selection
        diff_frame = ttk.LabelFrame(self.frame, text="Niveau de difficulté", padding="10")
        diff_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        for i, level in enumerate(["Facile", "Moyen", "Difficile", "Personnalisé"]):
            ttk.Radiobutton(
                diff_frame,
                text=level,
                value=level,
                variable=self.difficulty_var,
                command=self.toggle_custom_options
            ).grid(row=i, column=0, pady=5, padx=10, sticky=tk.W)

        # Custom game options
        self.custom_frame = ttk.LabelFrame(self.frame, text="Options personnalisées", padding="10")
        self.custom_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

        # Height input
        ttk.Label(self.custom_frame, text="Hauteur:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self.custom_frame, textvariable=self.height_var, width=10).grid(row=0, column=1, padx=5, pady=5)

        # Width input
        ttk.Label(self.custom_frame, text="Largeur:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self.custom_frame, textvariable=self.width_var, width=10).grid(row=1, column=1, padx=5, pady=5)

        # Mines input
        ttk.Label(self.custom_frame, text="Mines:").grid(row=2, column=0, padx=5, pady=5)
        ttk.Entry(self.custom_frame, textvariable=self.mines_var, width=10).grid(row=2, column=1, padx=5, pady=5)

        # Initially hide custom options
        self.custom_frame.grid_remove()

        # Buttons
        ttk.Button(self.frame, text="Nouvelle partie", command=self.start_game).grid(
            row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame, text="Meilleurs scores", command=self.on_show_scores).grid(
            row=4, column=0, columnspan=2, pady=10)

    def toggle_custom_options(self):
        """Show/hide custom game options based on difficulty selection."""
        if self.difficulty_var.get() == "Personnalisé":
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()

    def start_game(self):
        """Start a new game with selected options."""
        try:
            difficulty = self.difficulty_var.get()

            if difficulty == "Personnalisé":
                # Use custom values
                height = int(self.height_var.get())
                width = int(self.width_var.get())
                mines = int(self.mines_var.get())
            else:
                # Use predefined values
                settings = self.DIFFICULTY_LEVELS[difficulty]
                height = settings["height"]
                width = settings["width"]
                mines = settings["mines"]

            self.on_start_game(height, width, mines)

        except ValueError as e:
            messagebox.showerror("Erreur", "Veuillez entrer des nombres valides")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def destroy(self):
        """Clean up the UI elements."""
        if self.frame:
            self.frame.destroy()