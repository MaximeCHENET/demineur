class Cell:
    """Represents a single cell in the Minesweeper grid."""

    def __init__(self, x, y):
        """Initialize a new cell.

        Args:
            x (int): Row position
            y (int): Column position
        """
        self.x = x
        self.y = y
        self.is_mine = False      # Indicates if the cell contains a mine
        self.is_revealed = False  # Indicates if the cell has been clicked and revealed
        self.is_flagged = False   # Indicates if the cell has been marked with a flag
        self.adjacent_mines = 0   # Number of mines in adjacent cells
        self.button = None        # Reference to the cell's button widget in the UI

    def reveal(self):
        """Mark the cell as revealed when clicked."""
        self.is_revealed = True

    def toggle_flag(self):
        """Toggle the flagged state of the cell.

        Returns:
            bool: True if the flag state was changed, False if cell was already revealed
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False

    def place_mine(self):
        """Place a mine in this cell during board initialization."""
        self.is_mine = True

    def set_adjacent_mines(self, count):
        """Set the number of adjacent mines for this cell.

        Args:
            count (int): Number of mines in cells adjacent to this cell
        """
        self.adjacent_mines = count
