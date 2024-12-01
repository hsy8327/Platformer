import pygame
from pygame.examples.go_over_there import MAX_SPEED

from Platformer.src.player.movement import PlayerMovement


class PlayerCollisionHandler:
    def __init__(self, game):
        self.game = game
        self.in_sticky_ground = False  # 끈적한 지형 위에 있는지 체크

    def check_hazards(self, player):
        """
        위험 요소(가시, 골) 충돌 검사
        """
        # 가시 충돌 검사
        if not player.state.invincible and pygame.sprite.spritecollide(
                player, self.game.spikes, False
        ):
            player.take_damage()

        # 골 충돌 검사
        if pygame.sprite.spritecollide(player, self.game.goal, False):
            self.game.next_level()

    def check_collision(self, player, direction):
        """
        방향에 따른 충돌 검사를 수행합니다.
        """
        if direction == 'y':
            self._check_vertical_collision(player)
        elif direction == 'x':
            self._check_horizontal_collision(player)

        self._check_special_platforms(player)

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

        booster_hits = pygame.sprite.spritecollide(
            player, self.game.booster_pads, False
        )
        if booster_hits:
            player.rect.bottom = booster_hits[0].rect.top
            player.physics.vel_y = 0.1
            on_ground_this_frame = True
            booster_hits[0].apply_boost(player)

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

    def _check_special_platforms(self, player):
        # 끈적한 지형 체크
        sticky_hits = pygame.sprite.spritecollide(
            player, self.game.sticky_grounds, False
        )

        if sticky_hits and player.physics.on_ground:  # 땅에 닿아있을 때만 효과 적용
            if not self.in_sticky_ground:
                self.in_sticky_ground = True
                sticky_hits[0].apply_effect(player)
        else:
            if self.in_sticky_ground:
                self.in_sticky_ground = False
                player.movement.remove_sticky_effect()