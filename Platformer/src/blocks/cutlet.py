import pygame

from Platformer.src.blocks.platform import Platform
from Platformer.src.settings import *


class Cutlet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/cutlet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass