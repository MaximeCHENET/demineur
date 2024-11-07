import random
from .cell import Cell


class GameBoard:
    """Represents the Minesweeper game board and manages game logic."""

    def __init__(self, height, width, mines):
        """Initialize a new game board.

        Args:
            height (int): Number of rows
            width (int): Number of columns
            mines (int): Number of mines to place
        """
        self.height = height
        self.width = width
        self.mines = mines
        self.cells = self._create_cells()
        self.game_started = False

    def _create_cells(self):
        """Create the grid of cells.

        Returns:
            list: 2D list of Cell objects
        """
        return [[Cell(x, y) for y in range(self.width)] for x in range(self.height)]

    def _get_safe_zone_positions(self, first_x, first_y):
        """Get positions that should be safe (no mines) around first click.

        Args:
            first_x (int): Row of first click
            first_y (int): Column of first click

        Returns:
            set: Set of (x,y) tuples representing safe positions
        """
        safe_positions = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = first_x + dx, first_y + dy
                if 0 <= new_x < self.height and 0 <= new_y < self.width:
                    safe_positions.add((new_x, new_y))
        return safe_positions

    def place_mines(self, first_x, first_y):
        """Place mines randomly on the board, avoiding the first clicked cell and its neighbors.

        Args:
            first_x (int): Row of first click
            first_y (int): Column of first click
        """
        # Get positions that should be safe (no mines)
        safe_positions = self._get_safe_zone_positions(first_x, first_y)

        # Get all possible positions excluding safe zone
        available_positions = [(x, y) for x in range(self.height) for y in range(self.width)
                             if (x, y) not in safe_positions]

        # Make sure we have enough positions for mines
        max_mines = len(available_positions)
        if self.mines > max_mines:
            self.mines = max_mines

        # Place mines randomly in available positions
        mine_positions = random.sample(available_positions, self.mines)

        for x, y in mine_positions:
            self.cells[x][y].place_mine()

        self._calculate_adjacent_mines()
        self.game_started = True

    def _calculate_adjacent_mines(self):
        """Calculate the number of adjacent mines for each cell."""
        for x in range(self.height):
            for y in range(self.width):
                if not self.cells[x][y].is_mine:
                    count = self._count_adjacent_mines(x, y)
                    self.cells[x][y].set_adjacent_mines(count)

    def _count_adjacent_mines(self, x, y):
        """Count mines in cells adjacent to the given position.

        Args:
            x (int): Row position
            y (int): Column position

        Returns:
            int: Number of adjacent mines
        """
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.height and
                        0 <= new_y < self.width and
                        self.cells[new_x][new_y].is_mine):
                    count += 1
        return count

    def reveal_cell(self, x, y):
        """Reveal a cell and recursively reveal adjacent cells if empty.

        Args:
            x (int): Row position
            y (int): Column position

        Returns:
            list: List of (x,y) coordinates of revealed cells
        """
        cell = self.cells[x][y]
        if cell.is_revealed or cell.is_flagged:
            return []

        revealed_cells = [(x, y)]
        cell.reveal()

        # If cell is empty, reveal adjacent cells
        if cell.adjacent_mines == 0 and not cell.is_mine:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < self.height and
                            0 <= new_y < self.width):
                        revealed_cells.extend(self.reveal_cell(new_x, new_y))

        return revealed_cells

    def check_win(self):
        """Check if the game has been won.

        Returns:
            bool: True if all non-mine cells are revealed and all mines are flagged
        """
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    return False
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True