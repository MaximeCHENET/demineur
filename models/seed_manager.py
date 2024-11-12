import json
from pathlib import Path
import time

class SeedManager:
    def __init__(self, seeds_file="board_seeds.json"):
        self.seeds_file = Path(seeds_file)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not self.seeds_file.exists():
            self.seeds_file.write_text('[]')

    def save_seed(self, seed, width, height, mines, first_click):
        seeds = []
        if self.seeds_file.exists():
            with open(self.seeds_file, 'r') as f:
                seeds = json.load(f)

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
        if not self.seeds_file.exists():
            return []

        with open(self.seeds_file, 'r') as f:
            seeds = json.load(f)

        return seeds[-limit:][::-1]
