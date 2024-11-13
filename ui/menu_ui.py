import tkinter as tk
from tkinter import ttk, messagebox
from .replay_dialog import ReplayDialog


class MenuUI:
    """Main menu interface for the Minesweeper game."""

    DIFFICULTY_LEVELS = {
        "Facile": {"height": 10, "width": 10, "mines": 10},
        "Moyen": {"height": 16, "width": 16, "mines": 40},
        "Difficile": {"height": 16, "width": 30, "mines": 99}
    }

    # Personalised mode limits
    CUSTOM_LIMITS = {
        "height": {"min": 5, "max": 30},
        "width": {"min": 5, "max": 35},
        "mines": {"min": 1, "max": 500}
    }

    def __init__(self, root, on_start_game, on_show_scores, on_replay_game):
        """Initialize the menu UI.

        Args:
            root: Tkinter root window
            on_start_game: Callback for starting a new game
            on_show_scores: Callback for showing high scores
            on_replay_game: Callback for replaying a previous game
        """
        self.root = root
        self.on_start_game = on_start_game
        self.on_show_scores = on_show_scores
        self.on_replay_game = on_replay_game
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
        height_entry = ttk.Entry(self.custom_frame, textvariable=self.height_var, width=10)
        height_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.custom_frame,
                  text=f"(min: {self.CUSTOM_LIMITS['height']['min']}, max: {self.CUSTOM_LIMITS['height']['max']})").grid(
            row=0, column=2, padx=5, pady=5)

        # Width input
        ttk.Label(self.custom_frame, text="Largeur:").grid(row=1, column=0, padx=5, pady=5)
        width_entry = ttk.Entry(self.custom_frame, textvariable=self.width_var, width=10)
        width_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.custom_frame,
                  text=f"(min: {self.CUSTOM_LIMITS['width']['min']}, max: {self.CUSTOM_LIMITS['width']['max']})").grid(
            row=1, column=2, padx=5, pady=5)

        # Mines input
        ttk.Label(self.custom_frame, text="Mines:").grid(row=2, column=0, padx=5, pady=5)
        mines_entry = ttk.Entry(self.custom_frame, textvariable=self.mines_var, width=10)
        mines_entry.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.custom_frame,
                  text=f"(min: {self.CUSTOM_LIMITS['mines']['min']}, max: {self.CUSTOM_LIMITS['mines']['max']})").grid(
            row=2, column=2, padx=5, pady=5)

        # Initially hide custom options
        self.custom_frame.grid_remove()

        # Buttons frame
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

        # Game buttons
        ttk.Button(buttons_frame, text="Nouvelle partie", command=self.start_game).grid(
            row=0, column=0, pady=5, padx=5)
        ttk.Button(buttons_frame, text="Rejouer une partie", command=self.on_replay_game).grid(
            row=0, column=1, pady=5, padx=5)
        ttk.Button(buttons_frame, text="Meilleurs scores", command=self.on_show_scores).grid(
            row=0, column=2, pady=5, padx=5)
        ttk.Button(buttons_frame, text="Quitter", command=self.quit_game, style="Quit.TButton").grid(
            row=1, column=0, columnspan=3, pady=10)

        # Quit button style
        style = ttk.Style()
        style.configure("Quit.TButton", foreground="red")

    def validate_custom_values(self, height, width, mines):
        """Validate custom game configuration values against defined limits.

        Args:
            height (int): Board height
            width (int): Board width
            mines (int): Number of mines

        Raises:
            ValueError: If any value is outside its defined limits
        """
        # Verify height limits
        if not self.CUSTOM_LIMITS["height"]["min"] <= height <= self.CUSTOM_LIMITS["height"]["max"]:
            raise ValueError(
                f"La hauteur doit être entre {self.CUSTOM_LIMITS['height']['min']} et {self.CUSTOM_LIMITS['height']['max']}")

        # Verify width limits
        if not self.CUSTOM_LIMITS["width"]["min"] <= width <= self.CUSTOM_LIMITS["width"]["max"]:
            raise ValueError(
                f"La largeur doit être entre {self.CUSTOM_LIMITS['width']['min']} et {self.CUSTOM_LIMITS['width']['max']}")

        # Verify limits of mines
        if not self.CUSTOM_LIMITS["mines"]["min"] <= mines <= self.CUSTOM_LIMITS["mines"]["max"]:
            raise ValueError(
                f"Le nombre de mines doit être entre {self.CUSTOM_LIMITS['mines']['min']} et {self.CUSTOM_LIMITS['mines']['max']}")

        # Verify that there is more cells than mines
        if mines >= (height * width):
            raise ValueError("Le nombre de mines doit être inférieur au nombre total de cases")

    def toggle_custom_options(self):
        """Show or hide custom game options based on difficulty selection.

        Displays custom options frame when 'Custom' difficulty is selected,
        hides it otherwise.
        """
        if self.difficulty_var.get() == "Personnalisé":
            self.custom_frame.grid()
        else:
            self.custom_frame.grid_remove()

    def start_game(self):
        """Start a new game with selected options.

        Validates game settings and initiates a new game with either
        predefined or custom configuration.
        """
        try:
            difficulty = self.difficulty_var.get()

            if difficulty == "Personnalisé":
                # Use custom values
                height = int(self.height_var.get())
                width = int(self.width_var.get())
                mines = int(self.mines_var.get())
                # Validate custom values
                self.validate_custom_values(height, width, mines)
            else:
                # Use predefined values
                settings = self.DIFFICULTY_LEVELS[difficulty]
                height = settings["height"]
                width = settings["width"]
                mines = settings["mines"]

            self.on_start_game(height, width, mines)

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def quit_game(self):
        """Quit the game after user confirmation.

        Displays confirmation dialog before closing the application.
        """
        if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter le jeu ?"):
            self.root.quit()

    def destroy(self):
        """Clean up and remove all UI elements."""
        if self.frame:
            self.frame.destroy()