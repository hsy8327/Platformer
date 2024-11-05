import pygame
from .player import Player
from .settings import *
from .level_loader import LevelLoader
from .platform import Platform


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("test")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'menu'

        # 스프라이트 그룹
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = None

        # 구름 및 학교 이미지 로드
        self.cloud_image = pygame.image.load(CLOUD_PATH).convert_alpha()
        self.school_image = pygame.image.load(SCHOOL_IMG_PATH).convert_alpha()  # 학교 이미지 로드

        # 텍스트 깜박임 관련 설정
        self.show_text = True
        self.text_timer = 0
        self.text_blink_interval = 500

        # 음악 로드
        self.background_music = BACKGROUND_MUSIC_PATH

        # 폰트 및 이미지 로드
        self.font_path = FONT_PATH
        self.title_image = pygame.image.load(TITLE_IMG_PATH).convert_alpha()

        # 카메라 오프셋
        self.camera_offset = 0

        # 고정된 배경 만들기
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.draw_fixed_background(self.background)

    def load_game(self):
        self.state = 'game'
        self.current_level = 1
        self.all_sprites.empty()
        self.platforms.empty()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.load_level(f'levels/level{self.current_level}.json')

        #배경음악 재생
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

    def load_level(self, level_file):
        level_loader = LevelLoader(self, level_file)
        level_loader.load_level()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            if self.state == 'menu':
                self.menu_events()
                self.menu_draw()
            elif self.state == 'game':
                self.events()
                self.update()
                self.draw()
        pygame.quit()

    # todo 외부로 뺄 코드
    def update_camera(self):
        # 플레이어가 화면 중간에 닿을 때만 카메라 이동, 왼쪽으로는 이동하지 않음
        self.camera_offset = -(self.player.rect.centerx - SCREEN_WIDTH // 2)
        if self.camera_offset > 0:
            self.camera_offset = 0

    def draw_fixed_background(self, surface):
        start_color = (0, 162, 255)
        end_color = (107, 239, 254)
        for y in range(SCREEN_HEIGHT):
            blend_ratio = y / SCREEN_HEIGHT
            blended_color = (
                int(start_color[0] + (end_color[0] - start_color[0]) * blend_ratio),
                int(start_color[1] + (end_color[1] - start_color[1]) * blend_ratio),
                int(start_color[2] + (end_color[2] - start_color[2]) * blend_ratio),
            )
            pygame.draw.line(surface, blended_color, (0, y), (SCREEN_WIDTH, y))

        # 구름 이미지 (고정)
        surface.blit(self.cloud_image, (100, 50))
        surface.blit(self.cloud_image, (400, 100))

        # School 이미지 배치
        school_x = SCREEN_WIDTH - self.school_image.get_width() - 600  # x축
        school_y = SCREEN_HEIGHT - self.school_image.get_height() - 35  # y축
        surface.blit(self.school_image, (school_x, school_y))

    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.load_game()

    def menu_draw(self):
        self.screen.blit(self.background, (0, 0))
        logo_x = SCREEN_WIDTH // 2 - self.title_image.get_width() // 2
        logo_y = SCREEN_HEIGHT // 2 - self.title_image.get_height()
        self.screen.blit(self.title_image, (logo_x, logo_y))

        current_time = pygame.time.get_ticks()
        if current_time - self.text_timer > self.text_blink_interval:
            self.show_text = not self.show_text
            self.text_timer = current_time

        if self.show_text:
            font = pygame.font.Font(self.font_path, 20)
            text = font.render("Press Enter to Start", True, BLACK)
            text_x = SCREEN_WIDTH // 2 - text.get_width() // 2
            text_y = SCREEN_HEIGHT // 1.2 - text.get_height() // 2
            self.screen.blit(text, (text_x, text_y))

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.update_camera()

    def draw(self):
        self.screen.blit(self.background, (0, 0))  # 고정된 배경을 화면 전체에 배치
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x + self.camera_offset, sprite.rect.y))
        pygame.display.flip()