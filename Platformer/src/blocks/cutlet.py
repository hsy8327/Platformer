import pygame
from Platformer.src.settings import *
from Platformer.src.blocks.platform import Platform

class Cutlet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/prepImg/cutlet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))

    def update(self):
        pass