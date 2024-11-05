import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, PLAYER_JUMP_FORCE, GRAVITY, MAX_FALL_SPEED, PLAYER_IMG, \
    PLAYER_IMG_RIGHT_RUN, PLAYER_IMG_LEFT_RUN, PLAYER_IMG_RIGHT_JUMP, PLAYER_IMG_LEFT_JUMP, PLAYER_IMG_STANDING_LEFT, \
    PLAYER_IMG_STANDING_RIGHT, JUMPING_SOUND, RUNNING_SOUND


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game  # 게임 인스턴스 저장

        # 이미지 불러오기
        self.standing_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG).convert_alpha(), (64, 64))
        self.right_run_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_RIGHT_RUN).convert_alpha(), (64, 64))
        self.left_run_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_LEFT_RUN).convert_alpha(), (64, 64))
        self.right_jump_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_RIGHT_JUMP).convert_alpha(), (64, 64))
        self.left_jump_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_LEFT_JUMP).convert_alpha(), (64, 64))
        self.left_mario_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_STANDING_LEFT).convert_alpha(), (64, 64))
        self.right_mario_image = pygame.transform.scale(pygame.image.load(PLAYER_IMG_STANDING_RIGHT).convert_alpha(), (64, 64))

        self.image = self.standing_image
        self.rect = self.image.get_rect()

        # 위치 초기화
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT

        # 초기 속도 설정
        self.vel_x = 0
        self.vel_y = 0
        self.facing = "right"  # 캐릭터가 향하는 방향
        self.on_ground = False

        # 애니메이션 관련 변수
        self.frame_count = 0
        self.frame_delay = 5  # 프레임 전환 속도 설정

        # 사운드 로딩
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
            self.jump_sound.play()  # 점프할 때 사운드 실행

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

    def update(self):
        self.handle_input()
        self.apply_gravity()

        # 방향 및 속도에 따른 이미지 업데이트
        if self.vel_y < 0:  # 점프 중일 때
            if self.facing == "right":
                self.image = self.right_jump_image
            else:
                self.image = self.left_jump_image
        elif self.vel_x != 0 and self.on_ground:  # 이동 중이며 바닥에 있을 때
            if not self.is_running_sound_playing:
                self.running_sound.play(-1)  # 반복 재생
                self.is_running_sound_playing = True

            if self.vel_x > 0:  # 오른쪽으로 이동할 때
                self.frame_count += 1
                if self.frame_count >= self.frame_delay:
                    self.frame_count = 0
                    if self.image == self.right_mario_image:
                        self.image = self.right_run_image
                    else:
                        self.image = self.right_mario_image
            elif self.vel_x < 0:  # 왼쪽으로 이동할 때
                self.frame_count += 1
                if self.frame_count >= self.frame_delay:
                    self.frame_count = 0
                    if self.image == self.left_mario_image:
                        self.image = self.left_run_image
                    else:
                        self.image = self.left_mario_image
        else:  # 멈출 때 혹은 공중에 있을 때
            if self.is_running_sound_playing:
                self.running_sound.stop()  # 사운드 멈춤
                self.is_running_sound_playing = False

            if self.facing == "right":
                self.image = self.right_mario_image
            elif self.facing == "left":
                self.image = self.left_mario_image
            else:
                self.image = self.standing_image

        self.rect.x += self.vel_x
        self.check_collision('x')

        self.rect.y += self.vel_y
        self.check_collision('y')

        # 화면 경계 체크 (좌우)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def check_collision(self, direction):
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        if hits:
            if direction == 'x':
                if self.vel_x > 0:
                    self.rect.right = hits[0].rect.left
                elif self.vel_x < 0:
                    self.rect.left = hits[0].rect.right
                self.vel_x = 0
            elif direction == 'y':
                if self.vel_y > 0:
                    self.rect.bottom = hits[0].rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = hits[0].rect.bottom
                    self.vel_y = 0
        else:
            if direction == 'y':
                self.on_ground = False
                #self.vel 사용해서 바닥에서 걸어다닐 때만 running-sound.mp3가 나오도록 설정 (공중에서 떨어지는 과정에서도 걸어다니는 사운드가 겹쳐서 일단 수정)