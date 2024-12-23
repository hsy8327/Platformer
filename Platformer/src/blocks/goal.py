import pygame
from Platformer.src.settings import *
from Platformer.src.blocks.platform import Platform


class Goal(Platform):
    def _load_image(self, image):
        if image is None:
            image = pygame.image.load('assets/platforms/goal.png').convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return image

    def update(self):
        pass
