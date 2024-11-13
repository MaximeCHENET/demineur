import json
from pathlib import Path
import time

class SeedManager:
    """Manages game board seeds for replay functionality."""

    def __init__(self, seeds_file="board_seeds.json"):
        """Initialize the seed manager.

        Args:
            seeds_file (str): Path to the seeds storage file
        """
        self.seeds_file = Path(seeds_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the seeds file if it doesn't exist."""
        if not self.seeds_file.exists():
            self.seeds_file.write_text('[]')

    def save_seed(self, seed, width, height, mines, first_click):
        """Save a board configuration for future replay.

        Args:
            seed (int): Random seed used for mine placement
            width (int): Board width
            height (int): Board height
            mines (int): Number of mines
            first_click (tuple): Coordinates of first click
        """
        seeds = []
        if self.seeds_file.exists():
            with open(self.seeds_file, 'r') as f:
                seeds = json.load(f)

        # Keep only the 5 most recent seeds
        if len(seeds) >= 5:
            seeds.pop(0)

        seed_data = {
            'seed': seed,
            'width': width,
            'height': height,
            'mines': mines,
            'first_click': first_click,
            'date': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        seeds.append(seed_data)

        with open(self.seeds_file, 'w') as f:
            json.dump(seeds, f)

    def get_recent_seeds(self, limit=5):
        """Get the most recent board configurations.

        Args:
            limit (int): Maximum number of seeds to return

        Returns:
            list: List of recent board configurations, newest first
        """
        if not self.seeds_file.exists():
            return []

        with open(self.seeds_file, 'r') as f:
            seeds = json.load(f)

        return seeds[-limit:][::-1]
