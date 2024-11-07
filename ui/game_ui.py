import tkinter as tk
from tkinter import ttk
from .score_dialog import ScoreDialog


class GameUI:
    """Manages the game board user interface."""

    # Color mapping for adjacent mine numbers
    NUMBER_COLORS = {
        1: '#0000FF',  # Blue
        2: '#008000',  # Green
        3: '#FF0000',  # Red
        4: '#000080',  # Dark Blue
        5: '#800000',  # Crimson
        6: '#008080',  # Cyan
        7: '#000000',  # Black
        8: '#808080'  # Grey
    }

    def __init__(self, root, game_board, on_cell_click, on_right_click, on_return_to_menu):
        """Initialize the game UI.

        Args:
            root: Tkinter root window
            game_board: GameBoard instance
            on_cell_click: Callback for left-click events
            on_right_click: Callback for right-click events
            on_return_to_menu: Callback for return to menu button
        """
        self.root = root
        self.game_board = game_board
        self.on_cell_click = on_cell_click
        self.on_right_click = on_right_click
        self.on_return_to_menu = on_return_to_menu
        self.frame = None
        self.timer_label = None
        self.create_game_board()

    def create_game_board(self):
        """Create the game board UI elements."""
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Timer label
        self.timer_label = ttk.Label(self.frame, text="Temps: 0s")
        self.timer_label.grid(row=0, column=0, columnspan=self.game_board.width, pady=5)

        # Create cell buttons
        style = {'width': 2, 'height': 1, 'font': ('TkDefaultFont', 10, 'bold')}

        for x in range(self.game_board.height):
            for y in range(self.game_board.width):
                cell = self.game_board.cells[x][y]
                cell.button = tk.Button(
                    self.frame,
                    **style,
                    text="",
                    bg='lightgray',
                    relief=tk.RAISED
                )
                cell.button.grid(row=x + 1, column=y)
                cell.button.bind('<Button-1>', lambda e, x=x, y=y: self.on_cell_click(x, y))
                cell.button.bind('<Button-3>', lambda e, x=x, y=y: self.on_right_click(x, y))

        # Return to menu button
        back_button = ttk.Button(self.frame, text="Retour au menu", command=self.on_return_to_menu)
        back_button.grid(row=self.game_board.height + 1, column=0, columnspan=self.game_board.width, pady=10)

    def update_cell(self, x, y):
        """Update the appearance of a cell based on its state.

        Args:
            x (int): Row position
            y (int): Column position
        """
        cell = self.game_board.cells[x][y]
        if cell.is_revealed:
            cell.button.config(
                relief=tk.SUNKEN,
                bg='white',
                state='disabled'
            )
            if cell.adjacent_mines > 0:
                cell.button.config(
                    text=str(cell.adjacent_mines),
                    fg=self.NUMBER_COLORS.get(cell.adjacent_mines, 'black'),
                    disabledforeground=self.NUMBER_COLORS.get(cell.adjacent_mines, 'black')
                )
        elif cell.is_flagged:
            cell.button.config(
                text='🚩',
                bg='red',
                relief=tk.RAISED
            )
        else:
            cell.button.config(
                text='',
                bg='lightgray',
                relief=tk.RAISED
            )

    def show_mines(self):
        """Reveal all mines on the board (game over state)."""
        for row in self.game_board.cells:
            for cell in row:
                if cell.is_mine:
                    cell.button.config(
                        text='💣',
                        bg='red',
                        relief=tk.SUNKEN,
                        state='disabled'
                    )
                else:
                    cell.button.config(state='disabled')

    def update_timer(self, elapsed_time):
        """Update the timer display.

        Args:
            elapsed_time (int): Time elapsed in seconds
        """
        if self.timer_label:
            self.timer_label.config(text=f"Temps: {elapsed_time}s")

    def destroy(self):
        """Clean up the UI elements."""
        if self.frame:
            self.frame.destroy()