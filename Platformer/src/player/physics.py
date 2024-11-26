from Platformer.src.settings import GRAVITY, MAX_FALL_SPEED, SCREEN_HEIGHT, TILE_SIZE

class PlayerPhysics:
    def __init__(self):
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        # 점프 관련 상수
        self.JUMP_VELOCITY = -10
        self.JUMP_RELEASE_VELOCITY = -3
        self.MAX_JUMP_HEIGHT = TILE_SIZE * 4
        self.DAMAGE_JUMP_VELOCITY = -150  # 데미지 시 점프 속도 (일반 점프보다 약하게)

        # 점프 상태
        self.is_jumping = False
        self.jump_pressed = False
        self.jump_start_y = 0

    def update(self, player):
        self._apply_gravity()
        self._update_position(player)
        self._check_fall_death(player)

    def _apply_gravity(self):
        if self.is_jumping:
            current_jump_height = self.jump_start_y - self.last_y
            if current_jump_height >= self.MAX_JUMP_HEIGHT:
                self.is_jumping = False

        if not self.is_jumping or self.vel_y > 0:
            self.vel_y += GRAVITY
            if self.vel_y > MAX_FALL_SPEED:
                self.vel_y = MAX_FALL_SPEED

    def _update_position(self, player):
        """플레이어의 위치를 업데이트하고 collision_handler를 통해 충돌을 체크합니다."""
        self.last_y = player.rect.bottom

        # X축 이동 및 충돌 체크
        player.rect.x += self.vel_x
        player.collision_handler.check_collision(player, 'x')

        # Y축 이동 및 충돌 체크
        player.rect.y += self.vel_y
        player.collision_handler.check_collision(player, 'y')

    def _check_fall_death(self, player):
        """낙사 체크"""
        if player.rect.top > SCREEN_HEIGHT + TILE_SIZE:
            player.take_damage()
            player.reset_position()
