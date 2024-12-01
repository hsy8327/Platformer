# sticky_ground.py
from Platformer.src.blocks.platform import Platform
from Platformer.src.settings import *

class StickyGround(Platform):
    def __init__(self, x, y, image=None):
        super().__init__(x, y, image)
        self.slow_factor = 0.1  # 이동 속도 감소 비율

    def _load_image(self, image):
        if image is None:
            image = pygame.image.load('assets/platforms/sticky.png').convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return image

    def update(self):
        pass

    def apply_effect(self, player):
        # 현재 속도를 감소시킴
        player.movement.current_speed *= self.slow_factor
        # 최대 속도도 일시적으로 감소
        player.movement.WALK_MAX_SPEED *= self.slow_factor
        player.movement.RUN_MAX_SPEED *= self.slow_factor