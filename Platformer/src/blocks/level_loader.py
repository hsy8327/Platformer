import json

from Platformer.src.blocks.pathable_platforms import PathablePlatforms
from Platformer.src.blocks.platform import Platform
from Platformer.src.blocks.breakable_block import BreakableBlock
from Platformer.src.blocks.spike import Spike

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

        for pathable_platforms_data in data.get('pathable_platforms', []):
            pathable_platform = PathablePlatforms(
                pathable_platforms_data['x'],
                pathable_platforms_data['y'],
            )
            self.game.all_sprites.add(pathable_platform)
            self.game.breakable_blocks.add(pathable_platform)

        for spikes_data in data.get('spikes', []):
            spikes = Spike(
                spikes_data['x'],
                spikes_data['y']
            )
            self.game.all_sprites.add(spikes)
            self.game.spikes.add(spikes)