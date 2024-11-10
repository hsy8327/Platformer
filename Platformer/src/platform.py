import pygame
from .settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, image=None):
        super().__init__()
        if image:
            self.image = pygame.transform.scale(pygame.image.load(image), (TILE_SIZE, TILE_SIZE))
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.image.fill(GREEN)

        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
