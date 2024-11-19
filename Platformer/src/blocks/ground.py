import pygame
from Platformer.src.blocks.platform import Platform
from Platformer.src.settings import *

class Ground(Platform):
    def _load_image(self, image):
        if image is None:
            image = pygame.image.load('assets/platforms/floor.png').convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return image

    def update(self):
        pass