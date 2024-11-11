from .platform import Platform
from Platformer.src.settings import *

class Spike(Platform):
    def __init__(self, x, y, image=None):
        if image is None:
            image = pygame.image.load('assets/platforms/spike.png').convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE,TILE_SIZE))
        super().__init__(x, y, image)

