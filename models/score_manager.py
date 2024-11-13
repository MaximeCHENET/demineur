# score_manager.py
import json
from pathlib import Path
import time


class ScoreManager:
    """Manages high scores for the Minesweeper game."""

    def __init__(self, scores_file="high_scores.json"):
        """Initialize the score manager.

        Args:
            scores_file (str): Path to the scores storage file
        """
        self.scores_file = Path(scores_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the scores file if it doesn't exist."""
        if not self.scores_file.exists():
            with open(self.scores_file, 'w') as f:
                json.dump([], f)

    def save_score(self, player_name, elapsed_time, width, height, mines, seed, first_click):
        """Save a new score to the high scores file.

        Args:
            player_name (str): Name of the player
            elapsed_time (int): Time taken to complete the game
            width (int): Board width
            height (int): Board height
            mines (int): Number of mines
            seed (int): Board seed for replay
            first_click (tuple): First click coordinates for replay
        """
        scores = []
        if self.scores_file.exists():
            with open(self.scores_file, 'r') as f:
                scores = json.load(f)

        new_score = {
            'name': player_name,
            'time': elapsed_time,
            'width': width,
            'height': height,
            'mines': mines,
            'date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'seed': seed,
            'first_click': first_click
        }

        scores.append(new_score)
        # Sort scores by board configuration and then by completion time
        scores.sort(key=lambda x: (
            x['width'],
            x['height'],
            x['mines'],
            x['time']
        ))

        with open(self.scores_file, 'w') as f:
            json.dump(scores, f)

    def get_high_scores(self):
        """Retrieve all high scores.

        Returns:
            list: List of high score dictionaries, sorted by configuration and time
        """
        if not self.scores_file.exists():
            return []

        with open(self.scores_file, 'r') as f:
            scores = json.load(f)

        return scores