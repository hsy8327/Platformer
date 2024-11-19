import json

from Platformer.src.blocks.ground import Ground
from Platformer.src.blocks.pathable_platforms import PathablePlatforms
from Platformer.src.blocks.platform import Platform
from Platformer.src.blocks.breakable_block import BreakableBlock
from Platformer.src.blocks.spike import Spike
from Platformer.src.blocks.goal import Goal

class LevelLoader:
    def __init__(self, game, level_file):
        self.game = game
        self.level_file = level_file

    def load_level(self):
        with open(self.level_file, 'r') as f:
            data = json.load(f)

        for ground_data in data.get('ground', []):
            ground = Ground(
                ground_data['x'],
                ground_data['y'],
            )
            self.game.all_sprites.add(ground)
            self.game.ground.add(ground)

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
            self.game.pathable_platforms.add(pathable_platform)

        for spikes_data in data.get('spikes', []):
            spikes = Spike(
                spikes_data['x'],
                spikes_data['y']
            )
            self.game.all_sprites.add(spikes)
            self.game.spikes.add(spikes)

        for goal_data in data.get('goal', []):
            goal = Goal(
                goal_data['x'],
                goal_data['y'],
            )
            self.game.all_sprites.add(goal)
            self.game.goal.add(goal)