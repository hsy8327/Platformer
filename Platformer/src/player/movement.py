import pygame
from Platformer.src.settings import TILE_SIZE


class PlayerMovement:
    def __init__(self):
        # 이동 관련 상수
        self.WALK_ACCELERATION = 0.5
        self.RUN_ACCELERATION = 0.8
        self.WALK_DECELERATION = 0.3
        self.WALK_MAX_SPEED = 8.0
        self.RUN_MAX_SPEED = 12.0

        # 상태 변수
        self.current_speed = 0.0
        self.is_running = False
        self.facing = "right"

    def handle_movement(self, physics, keys):
        self.is_running = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        acceleration = self.RUN_ACCELERATION if self.is_running else self.WALK_ACCELERATION
        max_speed = self.RUN_MAX_SPEED if self.is_running else self.WALK_MAX_SPEED

        if keys[pygame.K_LEFT]:
            self.current_speed = max(self.current_speed - acceleration, -max_speed)
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            self.current_speed = min(self.current_speed + acceleration, max_speed)
            self.facing = "right"
        else:
            self._handle_deceleration()

        physics.vel_x = self.current_speed

    def _handle_deceleration(self):
        if abs(self.current_speed) < self.WALK_DECELERATION:
            self.current_speed = 0
        elif self.current_speed > 0:
            self.current_speed -= self.WALK_DECELERATION
        else:
            self.current_speed += self.WALK_DECELERATION

    def handle_jump(self, player, physics, keys):
        if keys[pygame.K_SPACE]:
            if physics.on_ground and not physics.jump_pressed:
                self._start_jump(player, physics)
        else:
            self._end_jump(physics)

    def _start_jump(self, player, physics):
        physics.is_jumping = True
        physics.jump_pressed = True
        physics.vel_y = physics.JUMP_VELOCITY
        physics.jump_start_y = player.rect.bottom
        player.state.play_jump_sound()

    def _end_jump(self, physics):
        if physics.is_jumping and physics.vel_y < physics.JUMP_RELEASE_VELOCITY:
            physics.vel_y = physics.JUMP_RELEASE_VELOCITY
        physics.jump_pressed = False
        physics.is_jumping = False

