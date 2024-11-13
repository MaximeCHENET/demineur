import random
import time
from .cell import Cell


class GameBoard:
    def __init__(self, height, width, mines, seed=None, first_click=None):
        """Initialize the game board.

        Args:
            height (int): Number of rows in the board
            width (int): Number of columns in the board
            mines (int): Total number of mines to place
            seed (int, optional): Random seed for mine placement
            first_click (tuple, optional): Coordinates of first click for replay
        """
        self.height = height
        self.width = width
        self.mines = mines
        self.seed = seed if seed is not None else int(time.time())  # Use current time as default seed
        self.cells = self._create_cells()
        self.game_started = False                                   # Tracks if first click has occurred
        self.first_click_position = first_click                     # Stores first click for replays

        # Place mines immediately if first click is provided (replay mode)
        if first_click is not None:
            self.place_mines(*first_click)

    def _create_cells(self):
        """Create the initial grid of empty cells.

        Returns:
            list: 2D list of Cell objects
        """
        return [[Cell(x, y) for y in range(self.width)] for x in range(self.height)]

    def get_seed(self):
        """Get the current board's random seed.

        Returns:
            int: The seed used for mine placement
        """
        return self.seed

    def _get_safe_zone_positions(self, first_x, first_y):
        """Calculate positions that should not contain mines around first click.

        Args:
            first_x (int): Row of first click
            first_y (int): Column of first click

        Returns:
            set: Set of coordinate tuples marking safe positions
        """
        safe_positions = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = first_x + dx, first_y + dy
                if 0 <= new_x < self.height and 0 <= new_y < self.width:
                    safe_positions.add((new_x, new_y))
        return safe_positions

    def place_mines(self, first_x, first_y):
        """Place mines on the board, ensuring first click is safe.

        Args:
            first_x (int): Row of first click
            first_y (int): Column of first click
        """
        if self.first_click_position is None:
            self.first_click_position = (first_x, first_y)

        random.seed(self.seed)

        # Get positions that should be safe (around first click)
        safe_positions = self._get_safe_zone_positions(first_x, first_y)

        # Create list of all possible positions excluding safe zone
        available_positions = [(x, y) for x in range(self.height) for y in range(self.width)
                             if (x, y) not in safe_positions]

        # Adjust number of mines if there aren't enough available positions
        max_mines = len(available_positions)
        if self.mines > max_mines:
            self.mines = max_mines

        # Randomly place mines
        mine_positions = random.sample(available_positions, self.mines)
        for x, y in mine_positions:
            self.cells[x][y].place_mine()

        self._calculate_adjacent_mines()
        self.game_started = True

    def _calculate_adjacent_mines(self):
        """Calculate number of adjacent mines for all cells."""
        for x in range(self.height):
            for y in range(self.width):
                if not self.cells[x][y].is_mine:
                    count = self._count_adjacent_mines(x, y)
                    self.cells[x][y].set_adjacent_mines(count)

    def _count_adjacent_mines(self, x, y):
        """Count mines in cells adjacent to given position.

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
            list: List of coordinate tuples of all cells revealed
        """
        cell = self.cells[x][y]
        if cell.is_revealed or cell.is_flagged:
            return []

        revealed_cells = [(x, y)]
        cell.reveal()

        # Recursively reveal adjacent cells if current cell has no adjacent mines
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
            bool: True if all mines are flagged and all safe cells are revealed
        """
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    return False
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
