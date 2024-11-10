import pygame
from .platform import Platform
from .settings import *

class BreakableBlock(Platform):
    def __init__(self, x, y, image=None):
        if image is None:
            image = pygame.image.load('assets/platforms/brick.png').convert_alpha()
            image = pygame.transform.scale(image, (TILE_SIZE,TILE_SIZE))
        super().__init__(x, y, image)
        self.broken = False


    def break_block(self):
        self.broken = True
        self.kill()
        #Todo 이펙트 추가