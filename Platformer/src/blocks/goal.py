import pygame
from Platformer.src.settings import *
from Platformer.src.blocks.platform import Platform


class Goal(Platform):
    def __init__(self, x, y, image=None):
        if image is None:
            image = pygame.image.load('assets/platforms/goal.png').convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE,TILE_SIZE))
        super().__init__(x, y, image)