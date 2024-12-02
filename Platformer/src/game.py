import pygame.sprite

from Platformer.src.background_loader import BackgroundLoader
from Platformer.src.blocks.level_loader import LevelLoader
from Platformer.src.player.player import Player
from .settings import *


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
        self.ground = pygame.sprite.Group()
        self.breakable_blocks = pygame.sprite.Group()
        self.pathable_platforms = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.booster_pads = pygame.sprite.Group()
        self.solid_blocks = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.player = None

        # 텍스트 깜박임 관련 설정
        self.show_text = True
        self.text_timer = 0
        self.text_blink_interval = 500

        # 음악 로드
        self.background_music = BACKGROUND_MUSIC_PATH

        # 레벨 로드
        self.current_level = 0

        # 폰트 및 이미지 로드
        self.font_path = FONT_PATH
        self.title_image = pygame.image.load(TITLE_IMG_PATH).convert_alpha()

        # 카메라 오프셋
        self.camera_offset = 0

        # BackgroundLoader 인스턴스 생성
        self.background_loader = BackgroundLoader(self, 'assets/backgrounds/background1.json')

    def load_game(self):
        self.state = 'game'
        self.current_level = 1
        self.all_sprites.empty()
        self.platforms.empty()
        self.ground.empty()
        self.breakable_blocks.empty()
        self.pathable_platforms.empty()
        self.spikes.empty()
        self.booster_pads.empty()
        self.solid_blocks.empty()
        self.goal.empty()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.load_level(f'levels/level{self.current_level}.json')

        # 배경음악 재생
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

    def load_level(self, level_file):
        level_loader = LevelLoader(self, level_file)
        self.ground.empty()
        self.breakable_blocks.empty()
        self.pathable_platforms.empty()
        self.spikes.empty()
        self.booster_pads.empty()
        self.solid_blocks.empty()
        self.goal.empty()
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

    def update_camera(self):
        # 플레이어가 화면 중간에 닿을 때만 카메라 이동, 왼쪽으로는 이동하지 않음
        self.camera_offset = -(self.player.rect.centerx - SCREEN_WIDTH // 2)
        if self.camera_offset > 0:
            self.camera_offset = 0

    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.load_game()

    def menu_draw(self):
        self.screen.fill((0, 0, 0))  # 배경을 검은색으로 채우기
        self.background_loader.draw(self.screen, 0)  # 메뉴에서 배경을 그리기
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
        # 움직이는 배경을 화면에 그리기 (카메라 오프셋 적용)
        self.screen.fill((0, 0, 0))  # 전체 화면을 검은색으로 채워 초기화
        self.background_loader.draw(self.screen, self.camera_offset)

        # 스프라이트 그리기
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x + self.camera_offset, sprite.rect.y))

        # 라이프와 속도 정보 그리기
        self.draw_lives()
        self.draw_speed()
        pygame.display.flip()

    def draw_lives(self):
        font = pygame.font.Font(self.font_path, 20)
        text = font.render(f"Lives: {self.player.state.lives}", True, BLACK)
        self.screen.blit(text, (10, 10))

    def draw_speed(self):
        font = pygame.font.Font(self.font_path, 10)
        text = font.render(f"Speed: {self.player.movement.current_speed:.2f}", True, BLACK)
        self.screen.blit(text, (200, 10))

    def next_level(self):
        self.current_level += 1
        level_file = f'levels/level{self.current_level}.json'
        # 레벨 파일이 존재하는지 확인
        try:
            open(level_file, 'r').close()
        except FileNotFoundError:
            self.running = False  # 현재는 다음 레벨이 없으면 종료
            return

        self.all_sprites.empty()
        self.platforms.empty()
        self.pathable_platforms.empty()
        self.breakable_blocks.empty()
        self.spikes.empty()
        self.goal.empty()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        self.load_level(level_file)
