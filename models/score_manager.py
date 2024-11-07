import json
from pathlib import Path
import time


class ScoreManager:
    """Manages high scores for the Minesweeper game."""

    def __init__(self, scores_file="high_scores.json"):
        """Initialize the score manager.

        Args:
            scores_file (str): Path to the scores file
        """
        self.scores_file = Path(scores_file)

    def save_score(self, player_name, elapsed_time, width, height, mines):
        """Save a new score to the high scores file.

        Args:
            player_name (str): Name of the player
            elapsed_time (int): Time taken to complete the game
            width (int): Board width
            height (int): Board height
            mines (int): Number of mines
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
            'date': time.strftime('%Y-%m-%d %H:%M:%S')
        }

        scores.append(new_score)
        scores.sort(key=lambda x: x['time'])

        with open(self.scores_file, 'w') as f:
            json.dump(scores, f)

    def get_high_scores(self, limit=10):
        """Retrieve the high scores.

        Args:
            limit (int): Maximum number of scores to return

        Returns:
            list: List of high score dictionaries
        """
        if not self.scores_file.exists():
            return []

        with open(self.scores_file, 'r') as f:
            scores = json.load(f)

        return scores[:limit]