import random
import time
from .cell import Cell


class GameBoard:
    def __init__(self, height, width, mines, seed=None, first_click=None):
        self.height = height
        self.width = width
        self.mines = mines
        self.seed = seed if seed is not None else int(time.time())
        self.cells = self._create_cells()
        self.game_started = False
        self.first_click_position = first_click

        if first_click is not None:
            self.place_mines(*first_click)

    def _create_cells(self):
        return [[Cell(x, y) for y in range(self.width)] for x in range(self.height)]

    def get_seed(self):
        return self.seed

    def _get_safe_zone_positions(self, first_x, first_y):
        safe_positions = set()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = first_x + dx, first_y + dy
                if 0 <= new_x < self.height and 0 <= new_y < self.width:
                    safe_positions.add((new_x, new_y))
        return safe_positions

    def place_mines(self, first_x, first_y):
        if self.first_click_position is None:
            self.first_click_position = (first_x, first_y)

        random.seed(self.seed)

        safe_positions = self._get_safe_zone_positions(first_x, first_y)

        available_positions = [(x, y) for x in range(self.height) for y in range(self.width)
                               if (x, y) not in safe_positions]

        max_mines = len(available_positions)
        if self.mines > max_mines:
            self.mines = max_mines

        mine_positions = random.sample(available_positions, self.mines)

        for x, y in mine_positions:
            self.cells[x][y].place_mine()

        self._calculate_adjacent_mines()
        self.game_started = True

    def _calculate_adjacent_mines(self):
        for x in range(self.height):
            for y in range(self.width):
                if not self.cells[x][y].is_mine:
                    count = self._count_adjacent_mines(x, y)
                    self.cells[x][y].set_adjacent_mines(count)

    def _count_adjacent_mines(self, x, y):
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
        cell = self.cells[x][y]
        if cell.is_revealed or cell.is_flagged:
            return []

        revealed_cells = [(x, y)]
        cell.reveal()

        if cell.adjacent_mines == 0 and not cell.is_mine:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < self.height and
                            0 <= new_y < self.width):
                        revealed_cells.extend(self.reveal_cell(new_x, new_y))

        return revealed_cells

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    return False
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
