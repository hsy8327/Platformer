from Platformer.src.blocks.platform import Platform
from Platformer.src.settings import *

class PathablePlatforms(Platform):
    def __init__(self, x, y, image=None):
        if image is None:
            image = pygame.image.load('assets/platforms/pathable_platform.png').convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE,TILE_SIZE))
        super().__init__(x, y, image)

    def break_block(self):
        self.broken = False
