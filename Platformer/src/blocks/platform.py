import pygame
from Platformer.src.settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        if image is None:
            image = pygame.image.load('assets/platforms/floor.png').convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE,TILE_SIZE))

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        super().__init__()