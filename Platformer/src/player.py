import pygame
from .settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY, MAX_FALL_SPEED, TILE_SIZE,
    PLAYER_IMG, PLAYER_IMG_RIGHT_RUN, PLAYER_IMG_LEFT_RUN,
    PLAYER_IMG_RIGHT_JUMP, PLAYER_IMG_LEFT_JUMP,
    PLAYER_IMG_STANDING_LEFT, PLAYER_IMG_STANDING_RIGHT,
    JUMPING_SOUND, RUNNING_SOUND
)


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self._load_images()
        self._initialize_physics()
        self._initialize_animation()
        self._initialize_sound()
        self._initialize_state()

    def _load_images(self):
        # 이미지 로딩 및 스케일링
        self.standing_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG).convert_alpha(),
                                                     (TILE_SIZE, TILE_SIZE))
        self.right_run_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_RIGHT_RUN).convert_alpha(),
                                                      (TILE_SIZE, TILE_SIZE))
        self.left_run_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_LEFT_RUN).convert_alpha(),
                                                     (TILE_SIZE, TILE_SIZE))
        self.right_jump_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_RIGHT_JUMP).convert_alpha(),
                                                       (TILE_SIZE, TILE_SIZE))
        self.left_jump_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_LEFT_JUMP).convert_alpha(),
                                                      (TILE_SIZE, TILE_SIZE))
        self.left_mario_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_STANDING_LEFT).convert_alpha(),
                                                       (TILE_SIZE, TILE_SIZE))
        self.right_mario_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_STANDING_RIGHT).convert_alpha(),
                                                        (TILE_SIZE, TILE_SIZE))

        self.image = self.standing_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT

    def _initialize_physics(self):
        # 물리 관련 변수
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False

        # 이동 관련 변수
        self.acceleration = 0.5
        self.deceleration = 0.3
        self.max_speed = 8.0
        self.current_speed = 0.0
        self.facing = "right"

        # 점프 관련 변수
        self.jump_velocity = -10  # 초기 점프 속도
        self.jump_release_velocity = -3  # 스페이스바를 떼었을 때의 최소 상승 속도
        self.is_jumping = False
        self.jump_pressed = False
        self.jump_start_y = 0  # 점프 시작 위치
        self.max_jump_height = TILE_SIZE * 4  # 최대 점프 높이 (4블록 높이)

    def _initialize_animation(self):
        self.frame_count = 0
        self.frame_delay = 5

    def _initialize_sound(self):
        self.jump_sound = pygame.mixer.Sound(JUMPING_SOUND)
        self.running_sound = pygame.mixer.Sound(RUNNING_SOUND)
        self.is_running_sound_playing = False

    def _initialize_state(self):
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2000

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self._handle_movement(keys)
        self._handle_jump(keys)

    def _handle_movement(self, keys):
        # 좌우 이동 처리
        if keys[pygame.K_LEFT]:
            self.current_speed = max(self.current_speed - self.acceleration, -self.max_speed)
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            self.current_speed = min(self.current_speed + self.acceleration, self.max_speed)
            self.facing = "right"
        else:
            # 감속 처리
            if abs(self.current_speed) < self.deceleration:
                self.current_speed = 0
            elif self.current_speed > 0:
                self.current_speed -= self.deceleration
            else:
                self.current_speed += self.deceleration

        self.vel_x = self.current_speed

    def _handle_jump(self, keys):
        if keys[pygame.K_SPACE]:
            if self.on_ground and not self.jump_pressed:
                # 점프 시작
                self.is_jumping = True
                self.jump_pressed = True
                self.vel_y = self.jump_velocity
                self.jump_start_y = self.rect.bottom  # 점프 시작 위치 저장
                self.jump_sound.play()
            elif self.is_jumping:
                # 최대 점프 높이 체크
                current_jump_height = self.jump_start_y - self.rect.bottom
                if current_jump_height < self.max_jump_height:
                    # 아직 최대 높이에 도달하지 않았다면 상승 유지
                    self.vel_y = self.jump_velocity
                else:
                    # 최대 높이 도달시 상승 중단
                    self.is_jumping = False
        else:
            # 스페이스바를 떼었을 때
            if self.is_jumping and self.vel_y < self.jump_release_velocity:
                self.vel_y = self.jump_release_velocity
            self.jump_pressed = False
            self.is_jumping = False

    def apply_gravity(self):
        # 최대 점프 높이 체크
        if self.is_jumping:
            current_jump_height = self.jump_start_y - self.rect.bottom
            if current_jump_height >= self.max_jump_height:
                self.is_jumping = False

        if not self.is_jumping or self.vel_y > 0:
            self.vel_y += GRAVITY
            if self.vel_y > MAX_FALL_SPEED:
                self.vel_y = MAX_FALL_SPEED

    def update_animation(self):
        if self.vel_y < 0:  # 점프 중
            self.image = self.right_jump_image if self.facing == "right" else self.left_jump_image
        elif self.vel_x != 0 and self.on_ground:  # 달리는 중
            self._update_running_animation()
        else:  # 정지 상태
            self._update_standing_animation()

    def _update_running_animation(self):
        if not self.is_running_sound_playing:
            self.running_sound.play(-1)
            self.is_running_sound_playing = True

        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            if self.vel_x > 0:
                self.image = self.right_run_image if self.image == self.right_mario_image else self.right_mario_image
            else:
                self.image = self.left_run_image if self.image == self.left_mario_image else self.left_mario_image

    def _update_standing_animation(self):
        if self.is_running_sound_playing:
            self.running_sound.stop()
            self.is_running_sound_playing = False

        self.image = self.right_mario_image if self.facing == "right" else self.left_mario_image

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.update_animation()

        # 위치 업데이트 및 충돌 검사
        self.rect.x += self.vel_x
        self.check_collision('x')
        self.rect.y += self.vel_y
        self.check_collision('y')

        # 기타 업데이트
        self.check_spike_collision()
        self.check_goal_collosion()
        self.update_invincibility()

        # 애니메이션 속도 조절
        self.frame_delay = max(3, int(8 - abs(self.current_speed)))

        # 화면 경계 체크
        if self.rect.left < 0:
            self.rect.left = 0

    def check_collision(self, direction):
        if direction == 'y':
            on_ground_this_frame = False

            # 통과 가능한 플랫폼 충돌 체크
            pathable_platform_hits = pygame.sprite.spritecollide(self, self.game.pathable_platforms, False)
            if pathable_platform_hits and self.vel_y >= 0:
                self.rect.bottom = pathable_platform_hits[0].rect.top
                self.vel_y = 0
                self.is_jumping = False
                on_ground_this_frame = True

            # 지면 충돌 체크
            ground_hits = pygame.sprite.spritecollide(self, self.game.ground, False)
            if ground_hits:
                if self.vel_y > 0:
                    self.rect.bottom = ground_hits[0].rect.top
                    self.vel_y = 0
                    on_ground_this_frame = True
                elif self.vel_y < 0:
                    self.rect.top = ground_hits[0].rect.bottom
                    self.vel_y = 0

            # 부서지는 블록 충돌 체크
            block_hits = pygame.sprite.spritecollide(self, self.game.breakable_blocks, False)
            if block_hits:
                if self.vel_y < 0:
                    block_hits[0].break_block()
                    self.vel_y = 0
                else:
                    self.rect.bottom = block_hits[0].rect.top
                    self.vel_y = 0
                    on_ground_this_frame = True

            self.on_ground = on_ground_this_frame

        elif direction == 'x':
            # 지면 충돌 체크 (좌우)
            ground_hits = pygame.sprite.spritecollide(self, self.game.ground, False)
            if ground_hits:
                if self.vel_x > 0:
                    self.rect.right = ground_hits[0].rect.left
                else:
                    self.rect.left = ground_hits[0].rect.right
                self.vel_x = 0

    def check_spike_collision(self):
        if not self.invincible and pygame.sprite.spritecollide(self, self.game.spikes, False):
            self.take_damage()

    def check_goal_collosion(self):
        if pygame.sprite.spritecollide(self, self.game.goal, False):
            self.game.next_level()

    def take_damage(self):
        self.lives -= 1
        print(f"{self.lives} lives left")
        if self.lives <= 0:
            self.game_over()
        else:
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()

    def update_invincibility(self):
        if self.invincible and pygame.time.get_ticks() - self.invincible_timer > self.invincible_duration:
            self.invincible = False

    def reset_position(self):
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT

    def game_over(self):
        print("게임 오버!")
        self.lives = 3
        self.reset_position()