# breakable_block.py

import pygame
from .platform import Platform

class BreakableBlock(Platform):
    def __init__(self, x, y, image=None):
        super().__init__(x, y, image)
        self.broken = False

    def break_block(self):
        self.broken = True
        self.kill()
        #Todo 이펙트 추가