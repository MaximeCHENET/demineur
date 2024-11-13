import tkinter as tk
from tkinter import ttk
from .score_dialog import ScoreDialog


class GameUI:
    """Manages the game board user interface.

    This class handles the creation and management of the Minesweeper game board interface,
    including cell buttons, timer display, and game controls.
    """

    # Color mapping for cell numbers (indicating adjacent mines)
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
            root (tk.Tk): Tkinter root window
            game_board (GameBoard): Game board instance containing game state
            on_cell_click (callable): Callback for left-click cell events
            on_right_click (callable): Callback for right-click cell events
            on_return_to_menu (callable): Callback for return to menu button
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
        """Create and initialize the game board UI elements.

        Sets up the main game frame, timer display, seed display,
        cell buttons grid, and return to menu button.
        """
        # Create frame to center the grid
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create timer and seed display
        info_frame = ttk.Frame(self.frame)
        info_frame.grid(row=0, column=0, columnspan=self.game_board.width, pady=5)

        self.timer_label = ttk.Label(info_frame, text="Time: 0s")
        self.timer_label.pack(side=tk.LEFT, padx=5)

        seed_label = ttk.Label(info_frame, text=f"Seed: {self.game_board.get_seed()}")
        seed_label.pack(side=tk.LEFT, padx=5)

        # Define cell button style
        style = {'width': 2, 'height': 1, 'font': ('TkDefaultFont', 10, 'bold')}

        # Create cell buttons grid
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

        # Create centered return to menu button
        back_button = ttk.Button(self.frame, text="Return to Menu", command=self.on_return_to_menu)
        back_button.grid(row=self.game_board.height + 1, column=0, columnspan=self.game_board.width, pady=10)

    def update_cell(self, x, y):
        """Update the visual appearance of a cell based on its current state.

        Args:
            x (int): Row position of the cell
            y (int): Column position of the cell
        """
        cell = self.game_board.cells[x][y]
        if cell.is_revealed:
            # Configure revealed cell appearance
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
            # Configure flagged cell appearance
            cell.button.config(
                text='🚩',
                bg='light blue',
                relief=tk.RAISED
            )
        else:
            # Configure default cell appearance
            cell.button.config(
                text='',
                bg='lightgray',
                relief=tk.RAISED
            )

    def show_mines(self):
        """Reveal all mines on the board (game over state).

        Updates the appearance of mine cells to show bomb icons
        and disables all cell buttons.
        """
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
        """Update the timer display with current elapsed time.

        Args:
            elapsed_time (int): Time elapsed in seconds since game start
        """
        if self.timer_label:
            self.timer_label.config(text=f"Time: {elapsed_time}s")

    def destroy(self):
        """Clean up and remove all UI elements."""
        if self.frame:
            self.frame.destroy()