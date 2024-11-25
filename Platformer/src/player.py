import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_FORCE, GRAVITY, MAX_FALL_SPEED, PLAYER_IMG, \
    PLAYER_IMG_RIGHT_RUN, PLAYER_IMG_LEFT_RUN, PLAYER_IMG_RIGHT_JUMP, PLAYER_IMG_LEFT_JUMP, PLAYER_IMG_STANDING_LEFT, \
    PLAYER_IMG_STANDING_RIGHT, JUMPING_SOUND, RUNNING_SOUND, TILE_SIZE


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
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
        self.right_mario_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_STANDING_RIGHT).convert_alpha(),
                                                        (TILE_SIZE, TILE_SIZE))
        self.left_mario_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_STANDING_LEFT).convert_alpha(),
                                                       (TILE_SIZE, TILE_SIZE))
        self.image = self.standing_image
        self.rect = self.image.get_rect()

        # 위치 초기화
        self.rect.centerx = (SCREEN_WIDTH / 2) - 270
        self.rect.bottom = SCREEN_HEIGHT

        self.vel_x = 0
        self.vel_y = 0
        self.facing = "right"

        self.on_ground = False
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2000

        self.frame_count = 0
        self.frame_delay = 5

        self.jump_sound = pygame.mixer.Sound(JUMPING_SOUND)
        self.running_sound = pygame.mixer.Sound(RUNNING_SOUND)
        self.is_running_sound_playing = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -PLAYER_SPEED
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            self.vel_x = PLAYER_SPEED
            self.facing = "right"
        else:
            self.vel_x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -PLAYER_JUMP_FORCE
            self.on_ground = False
            self.jump_sound.play()

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.update_invincibility()

        if self.vel_y < 0:  # Jumping
            self.image = self.right_jump_image if self.facing == "right" else self.left_jump_image
        elif self.vel_x != 0 and self.on_ground:  # Running on ground
            if not self.is_running_sound_playing:
                self.running_sound.play(-1)
                self.is_running_sound_playing = True
            self.animate_running()
        else:  # Standing still or falling
            if self.is_running_sound_playing:
                self.running_sound.stop()
                self.is_running_sound_playing = False
            self.image = self.right_mario_image if self.facing == "right" else self.left_mario_image

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.check_collision('x')
        self.check_collision('y')

        # Limit player's x position to the created ground section (0 to 100)
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > 101 * TILE_SIZE - self.rect.width:
            self.rect.x = 101 * TILE_SIZE - self.rect.width

        self.check_spike_collision()
        self.check_goal_collision()

    def animate_running(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            if self.facing == "right":
                self.image = self.right_run_image if self.image != self.right_run_image else self.right_mario_image
            else:
                self.image = self.left_run_image if self.image != self.left_run_image else self.left_mario_image

    def check_collision(self, direction):
        if direction == 'y':
            on_ground_this_frame = False

            pathable_platform_hits = pygame.sprite.spritecollide(self, self.game.pathable_platforms, False)
            if pathable_platform_hits:
                if self.vel_y >= 0:
                    self.rect.bottom = pathable_platform_hits[0].rect.top
                    self.vel_y = 0
                    on_ground_this_frame = True

            ground_hits = pygame.sprite.spritecollide(self, self.game.ground, False)
            if ground_hits:
                if direction == 'x':
                    if self.vel_x > 0:
                        self.rect.right = ground_hits[0].rect.left
                    elif self.vel_x < 0:
                        self.rect.left = ground_hits[0].rect.right
                    self.vel_x = 0
                elif direction == 'y':
                    if self.vel_y > 0:
                        self.rect.bottom = ground_hits[0].rect.top
                        self.vel_y = 0
                        on_ground_this_frame = True
                    elif self.vel_y < 0:
                        self.rect.top = ground_hits[0].rect.bottom
                        self.vel_y = 0

            block_hits = pygame.sprite.spritecollide(self, self.game.breakable_blocks, False)
            if block_hits:
                if direction == 'x':
                    pass
                elif direction == 'y':
                    if self.vel_y < 0:
                        block_hits[0].break_block()
                        self.vel_y = 0
                    elif self.vel_y > 0:
                        self.rect.bottom = block_hits[0].rect.top
                        self.vel_y = 0
                        on_ground_this_frame = True

            if direction == 'y':
                self.on_ground = on_ground_this_frame

    def check_spike_collision(self):
        if not self.invincible:
            if pygame.sprite.spritecollide(self, self.game.spikes, False):
                self.take_damage()

    def check_goal_collision(self):
        if pygame.sprite.spritecollide(self, self.game.goal, False) and self.lives > 0:
            self.game.clear_time = pygame.time.get_ticks() - self.game.start_ticks
            self.game.state = 'level_clear'
            self.game.stop_sounds()

    def take_damage(self):
        self.lives -= 1
        print(f"{self.lives} lives left")
        if self.lives <= 0:
            self.game.state = 'game_over'
        else:
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()

    def update_invincibility(self):
        if self.invincible and pygame.time.get_ticks() - self.invincible_timer > self.invincible_duration:
            self.invincible = False