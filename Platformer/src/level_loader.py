import json
from .platform import Platform
from .breakable_block import BreakableBlock

class LevelLoader:
    def __init__(self, game, level_file):
        self.game = game
        self.level_file = level_file

    def load_level(self):
        with open(self.level_file, 'r') as f:
            data = json.load(f)

        for plat_data in data.get('ground', []):
            platform = Platform(
                plat_data['x'],
                plat_data['y'],
            )
            self.game.all_sprites.add(platform)
            self.game.platforms.add(platform)

        for block_data in data.get('breakable_blocks', []):
            block = BreakableBlock(
                block_data['x'],
                block_data['y'],
            )
            self.game.all_sprites.add(block)
            self.game.breakable_blocks.add(block)