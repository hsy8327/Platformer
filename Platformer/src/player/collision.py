import pygame

class PlayerCollisionHandler:
    def __init__(self, game):
        self.game = game

    def check_hazards(self, player):
        """
        위험 요소(가시, 골) 충돌 검사
        """
        # 가시 충돌 검사
        if not player.state.invincible and pygame.sprite.spritecollide(
                player, self.game.spikes, False
        ):
            self._handle_spike_collision(player)

        # 골 충돌 검사
        if pygame.sprite.spritecollide(player, self.game.goal, False):
            self.game.timer_running = False  # 타이머 멈추기
            self.game.next_level()  # 클리어 처리

    def check_collision(self, player, direction):
        """
        방향에 따른 충돌 검사를 수행합니다.
        """
        if direction == 'y':
            self._check_vertical_collision(player)
        elif direction == 'x':
            self._check_horizontal_collision(player)

    def _check_vertical_collision(self, player):
        """수직 방향 충돌 검사"""
        on_ground_this_frame = False

        # 통과 가능한 플랫폼 충돌 체크
        pathable_platform_hits = pygame.sprite.spritecollide(
            player, self.game.pathable_platforms, False
        )
        if pathable_platform_hits and player.physics.vel_y >= 0:
            player.rect.bottom = pathable_platform_hits[0].rect.top
            player.physics.vel_y = 0
            player.physics.on_ground = True
            on_ground_this_frame = True

        # 지면 충돌 체크
        ground_hits = pygame.sprite.spritecollide(
            player, self.game.ground, False
        )
        if ground_hits:
            if player.physics.vel_y > 0:  # 떨어지는 중
                player.rect.bottom = ground_hits[0].rect.top
                player.physics.vel_y = 0
                on_ground_this_frame = True
            elif player.physics.vel_y < 0:  # 점프 중
                player.rect.top = ground_hits[0].rect.bottom
                player.physics.vel_y = 0

        # 부서지는 블록 충돌 체크
        block_hits = pygame.sprite.spritecollide(
            player, self.game.breakable_blocks, False
        )
        if block_hits:
            if player.physics.vel_y < 0:  # 점프로 부딪힘
                block_hits[0].break_block()
                player.physics.vel_y = 0.1
            else:  # 위에 착지
                player.rect.bottom = block_hits[0].rect.top
                player.physics.vel_y = 0
                on_ground_this_frame = True

        player.physics.on_ground = on_ground_this_frame

    def _check_horizontal_collision(self, player):
        """수평 방향 충돌 검사"""
        # 지면 충돌 체크 (좌우)
        ground_hits = pygame.sprite.spritecollide(
            player, self.game.ground, False
        )
        if ground_hits:
            if player.physics.vel_x > 0:  # 오른쪽으로 이동 중
                player.rect.right = ground_hits[0].rect.left
            else:  # 왼쪽으로 이동 중
                player.rect.left = ground_hits[0].rect.right
            player.physics.vel_x = 0
            player.movement.current_speed = 0

    def _handle_spike_collision(self, player):
        """가시 충돌시 데미지와 넉백"""
        if player.state.lives > 0:  # 아직 살아있다면
            #self._force_damage_jump(player)
            player.take_damage()

    def _force_damage_jump(self, player):
        """데미지를 입었을 때의 강제 점프"""
        # 강제 점프 속도 설정
        player.physics.vel_y = player.physics.DAMAGE_JUMP_VELOCITY
        # 왼쪽으로 밀어내기
        player.physics.vel_x = -player.movement.DAMAGE_KNOCKBACK_SPEED
        # 점프 상태 설정
        player.physics.is_jumping = True
        player.movement.facing = "left"  # 왼쪽 방향으로 강제 전환
