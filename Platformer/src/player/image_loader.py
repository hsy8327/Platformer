import pygame

from Platformer.src.settings import (
    TILE_SIZE,
    PLAYER_IMG, PLAYER_IMG_RIGHT_RUN, PLAYER_IMG_LEFT_RUN,
    PLAYER_IMG_RIGHT_JUMP, PLAYER_IMG_LEFT_JUMP,
    PLAYER_IMG_STANDING_LEFT, PLAYER_IMG_STANDING_RIGHT
)


class PlayerImageLoader:
    def __init__(self):
        self.images = {}
        self._load_images()

    def _load_images(self):
        """모든 플레이어 이미지를 로드하고 크기를 조정합니다."""
        image_paths = {
            'standing': PLAYER_IMG,
            'right_run': PLAYER_IMG_RIGHT_RUN,
            'left_run': PLAYER_IMG_LEFT_RUN,
            'right_jump': PLAYER_IMG_RIGHT_JUMP,
            'left_jump': PLAYER_IMG_LEFT_JUMP,
            'standing_left': PLAYER_IMG_STANDING_LEFT,
            'standing_right': PLAYER_IMG_STANDING_RIGHT
        }

        for key, path in image_paths.items():
            self.images[key] = self._load_and_scale_image(path)

    def _load_and_scale_image(self, path):
        """개별 이미지를 로드하고 크기를 조정합니다."""
        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"이미지 로드 실패: {path}")
            print(f"에러: {e}")
            # 에러 발생 시 기본 표시할 이미지 생성
            surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            surface.fill((255, 0, 255))  # 마젠타 색상으로 채움
            return surface

    def get_image(self, key):
        """특정 키에 해당하는 이미지를 반환합니다."""
        if key not in self.images:
            print(f"Warning: Image key '{key}' not found")
            return self.images.get('standing')  # 기본 이미지 반환
        return self.images[key]

