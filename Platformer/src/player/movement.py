import pygame

from Platformer.src.arduino import ArduinoController


# movement.py 경로:Platformer/src/player/movement.py
class PlayerMovement:
    def __init__(self):
        # 이동 관련 상수
        self.WALK_ACCELERATION = 0.5
        self.RUN_ACCELERATION = 0.8
        self.WALK_DECELERATION = 0.3
        self.WALK_MAX_SPEED = 8.0
        self.RUN_MAX_SPEED = 12.0

        self.BOOSTED_MAX_SPEED = 25.0
        self.BOOST_DURATION = 500

        # 상태 변수
        self.current_speed = 0.0
        self.is_running = False
        self.is_boosted = False
        self.boost_start_time = 0
        self.facing = "right"

        # 아두이노 입력
        self.arduino_controller = ArduinoController()

    def handle_movement(self, physics, keys):
        left, right, space, shift = self.arduino_controller.get_input_state(keys)

        current_time = pygame.time.get_ticks()
        if physics.on_ground:
            if self.is_boosted and current_time - self.boost_start_time > self.BOOST_DURATION:
                self.is_boosted = False
                normal_max_speed = self.RUN_MAX_SPEED if self.is_running else self.WALK_MAX_SPEED
                if abs(self.current_speed) > normal_max_speed:
                    self.current_speed = normal_max_speed if self.current_speed > 0 else -normal_max_speed

        self.is_running = shift
        acceleration = self.RUN_ACCELERATION if self.is_running else self.WALK_ACCELERATION

        max_speed = self.BOOSTED_MAX_SPEED if self.is_boosted else (
            self.RUN_MAX_SPEED if self.is_running else self.WALK_MAX_SPEED)

        if left:
            self.current_speed = max(self.current_speed - acceleration, -max_speed)
            self.facing = "left"
        elif right:
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
        _, _, space, _ = self.arduino_controller.get_input_state(keys)

        if space:
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

    def apply_boost(self, speed):
        self.is_boosted = True
        self.current_speed = speed
        self.boost_start_time = pygame.time.get_ticks()
