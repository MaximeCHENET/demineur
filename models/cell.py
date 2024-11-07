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
        self.is_mine = False  # True if cell contains a mine
        self.is_revealed = False  # True if cell has been clicked
        self.is_flagged = False  # True if cell has been flagged
        self.adjacent_mines = 0  # Number of adjacent mines
        self.button = None  # Reference to the cell's button widget

    def reveal(self):
        """Mark the cell as revealed."""
        self.is_revealed = True

    def toggle_flag(self):
        """Toggle the flagged state of the cell.

        Returns:
            bool: True if the flag state was changed, False otherwise
        """
        if not self.is_revealed:
            self.is_flagged = not self.is_flagged
            return True
        return False

    def place_mine(self):
        """Place a mine in this cell."""
        self.is_mine = True

    def set_adjacent_mines(self, count):
        """Set the number of adjacent mines.

        Args:
            count (int): Number of mines adjacent to this cell
        """
        self.adjacent_mines = count