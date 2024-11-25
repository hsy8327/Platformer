import pygame
from Platformer.src.settings import *
from Platformer.src.blocks.platform import Platform

class Cutlet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/cutlet.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        pass