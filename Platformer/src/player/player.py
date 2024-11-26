from Platformer.src.player.animation import *
from Platformer.src.player.physics import *
from Platformer.src.player.movement import *
from Platformer.src.player.image_loader import *
from Platformer.src.player.collision import *
from Platformer.src.player.state import *
from Platformer.src.settings import *


# player.py (수정된 부분)
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # 컴포넌트 초기화
        self.image_loader = PlayerImageLoader()
        self.collision_handler = PlayerCollisionHandler(game)
        self.physics = PlayerPhysics()
        self.movement = PlayerMovement()
        self.animation = PlayerAnimation()
        self.state = PlayerState()

        # 기본 이미지와 rect 설정
        self.image = self.image_loader.get_image('standing')
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT

    def handle_input(self):
        """사용자 입력 처리"""
        keys = pygame.key.get_pressed()
        self.movement.handle_movement(self.physics, keys)
        self.movement.handle_jump(self, self.physics, keys)

        # 달리기 사운드 업데이트
        is_moving = abs(self.physics.vel_x) > 0
        self.state.update_running_sound(is_moving and self.physics.on_ground)

    def take_damage(self):
        """데미지 처리"""
        self.state.take_damage()
        if self.state.lives <= 0:
            self.game_over()

    def update(self):
        """매 프레임 업데이트"""
        self.handle_input()
        self.physics.update(self)
        self.animation.update(self, self.physics, self.movement)

        # 위험 요소 충돌 검사
        self.collision_handler.check_hazards(self)
        self.state.update_invincibility()

        # 화면 경계 체크
        if self.rect.left < 0:
            self.rect.left = 0

    def reset_position(self):
        """위치 초기화"""
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT
        self.physics.vel_x = 0
        self.physics.vel_y = 0
        self.movement.current_speed = 0

    def game_over(self):
        """게임 오버 처리"""
        print("게임 오버!")
        self.state.reset()
        self.reset_position()
