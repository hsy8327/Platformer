import pygame
from abc import ABC, abstractmethod
from Platformer.src.settings import *


class Platform(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, image=None):
        super().__init__()
        self.image = self._load_image(image)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.broken = False

    @abstractmethod
    def _load_image(self, image):

        pass

    @abstractmethod
    def update(self):
        # 각 블록 타입별 업데이트 로직을 구현
        pass