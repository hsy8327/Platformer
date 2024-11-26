import pygame

from Platformer.src.settings import *
from .platform import Platform


class Spike(Platform):
    def _load_image(self, image):
        if image is None:
            image = pygame.image.load('assets/platforms/spike.png').convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return image

    def update(self):
        pass