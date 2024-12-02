# booster_pad.py
import pygame

from Platformer.src.blocks.platform import Platform
from Platformer.src.settings import *


class BoosterPad(Platform):
    def __init__(self, x, y, direction="right", image=None):
        super().__init__(x, y, image)
        self.direction = direction
        self.boost_power = 25.0

    def _load_image(self, image):
        if image is None:
            image = pygame.image.load('assets/platforms/booster.png').convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return image

    def update(self):
        pass

    def apply_boost(self, player):
        if self.direction == "right":
            player.movement.apply_boost(self.boost_power)
        elif self.direction == "left":
            player.movement.apply_boost(-self.boost_power)

