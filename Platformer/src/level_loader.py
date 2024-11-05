import json
from .platform import Platform

class LevelLoader:
    def __init__(self, game, level_file):
        self.game = game
        self.level_file = level_file

    def load_level(self):
        with open(self.level_file, 'r') as f:
            data = json.load(f)

        for plat_data in data.get('platforms', []):
            platform = Platform(
                plat_data['x'],
                plat_data['y'],
                plat_data['image'],
            )
            self.game.all_sprites.add(platform)
            self.game.platforms.add(platform)
