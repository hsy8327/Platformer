
import pygame
from Platformer.src.player.animation import PlayerAnimation
from Platformer.src.player.collision import PlayerCollisionHandler
from Platformer.src.player.image_loader import PlayerImageLoader
from Platformer.src.player.movement import PlayerMovement
from Platformer.src.player.physics import PlayerPhysics
from Platformer.src.player.state import PlayerState
from Platformer.src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

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
        self.rect.centerx = SCREEN_WIDTH / 5
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
        if not self.state.invincible:  # 이미 무적 상태가 아닐 때만 처리
            self.state.take_damage()
            if self.state.lives <= 0:
                self.game.game_over()  # 생명이 다 닳으면 즉시 게임 오버

    def update(self):
        """매 프레임 업데이트"""
        self.handle_input()
        self.physics.update(self)
        self.animation.update(self, self.physics, self.movement)
        self.check_cutlet_collision()  # 커틀렛과의 충돌 체크
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
        self.game.game_over()

    def check_cutlet_collision(self):
        """커틀렛과의 충돌을 체크하여 플레이어 속도를 증가시킵니다."""
        cutlet_hits = pygame.sprite.spritecollide(self, self.game.cutlets, True)
        if cutlet_hits:
            print("커틀렛을 먹었습니다!")
            for cutlet in cutlet_hits:
                # 속도 증가 로직
                self.movement.WALK_ACCELERATION += 2  # 더 큰 값으로 설정
                self.movement.RUN_ACCELERATION += 2  # 더 큰 값으로 설정
                self.movement.WALK_MAX_SPEED += 1  # 걸음 속도의 최대값 증가
                self.movement.RUN_MAX_SPEED += 1  # 달리기 속도의 최대값 증가