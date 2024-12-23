import pygame.sprite

from Platformer.src.background_loader import BackgroundLoader
from Platformer.src.blocks.level_loader import LevelLoader
from Platformer.src.player.player import Player
from .settings import *


# game.py 경로: Platformer/src/game.py
class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self._initialize_screen()
        self._initialize_state()
        self._initialize_groups()
        self._initialize_assets()
        self._initialize_camera()

    def _initialize_screen(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("test")
        self.clock = pygame.time.Clock()
        self.running = True

    def _initialize_state(self):
        self.state = 'menu'
        self.show_text = True
        self.text_timer = 0
        self.text_blink_interval = 500
        self.current_level = 0

    def _initialize_groups(self):
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

    def _initialize_assets(self):
        self.background_music = BACKGROUND_MUSIC_PATH
        self.font_path = FONT_PATH
        self.title_image = pygame.image.load(TITLE_IMG_PATH).convert_alpha()
        self.background_loader = BackgroundLoader(self, 'assets/backgrounds/background1.json')

    def _initialize_camera(self):
        self.camera_offset = 0

    def load_game(self):
        self.state = 'game'
        self.current_level = 1
        self._reset_groups()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.load_level(f'levels/level{self.current_level}.json')

        # 배경음악 재생
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.play(-1)

    def _reset_groups(self):
        self.all_sprites.empty()
        self.platforms.empty()
        self.ground.empty()
        self.breakable_blocks.empty()
        self.pathable_platforms.empty()
        self.spikes.empty()
        self.booster_pads.empty()
        self.solid_blocks.empty()
        self.goal.empty()

    def load_level(self, level_file):
        level_loader = LevelLoader(self, level_file)
        self._clear_level_specific_groups()
        level_loader.load_level()

    def _clear_level_specific_groups(self):
        self.ground.empty()
        self.breakable_blocks.empty()
        self.pathable_platforms.empty()
        self.spikes.empty()
        self.booster_pads.empty()
        self.solid_blocks.empty()
        self.goal.empty()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            if self.state == 'menu':
                self._handle_menu()
            elif self.state == 'game':
                self._handle_game()
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_draw()
            elif self.state == 'clear':
                self.clear_events()
                self.clear_draw()
        pygame.quit()

    def load_next_level(self):
        self.next_level()

    def game_clear(self):
        self.state = 'clear'
        pygame.mixer.music.stop()
        self.player.state.stop_sounds()
        self.captured_surface = self.screen.copy()
        self.game_clear_overlay_alpha = 0

    def clear_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # 홈 메뉴로 돌아가기
                    self.state = 'menu'
                elif event.key == pygame.K_c:  # 다음 스테이지로 도전하기
                    self.load_next_level()

    def clear_draw(self):
        if self.captured_surface:
            self.screen.blit(self.captured_surface, (0, 0))  # 캡처한 화면 그리기

        # 클리어 메시지
        big_font = pygame.font.Font(self.font_path, 50)
        clear_text = big_font.render("클리어!", True, (255, 255, 255))
        clear_x = SCREEN_WIDTH // 2 - clear_text.get_width() // 2
        clear_y = SCREEN_HEIGHT // 3 - clear_text.get_height() // 2
        self.screen.blit(clear_text, (clear_x, clear_y))

        # 홈 및 도전 버튼
        small_font = pygame.font.Font(self.font_path, 30)

        # 홈으로 돌아가기 버튼
        home_text = small_font.render("홈으로 돌아가기 (H)", True, (255, 255, 255))
        home_x = SCREEN_WIDTH // 2 - home_text.get_width() // 2
        home_y = clear_y + 100  # 저장하기 버튼 위쪽에 위치
        self.screen.blit(home_text, (home_x, home_y))
        self.home_button_rect = home_text.get_rect(center=(SCREEN_WIDTH // 2, home_y))  # 홈 버튼 위치

        # 도전하기 버튼
        challenge_text = small_font.render("도전하기 (C)", True, (255, 255, 255))
        challenge_x = SCREEN_WIDTH // 2 - challenge_text.get_width() // 2
        challenge_y = home_y + 50  # 홈 위쪽에 위치
        self.screen.blit(challenge_text, (challenge_x, challenge_y))

        pygame.display.flip()

    def _handle_menu(self):
        self.menu_events()
        self.menu_draw()

    def _handle_game(self):
        self.events()
        self.update()
        self.draw()

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
        self._draw_title_logo()
        self._draw_menu_text()
        pygame.display.flip()

    def _draw_title_logo(self):
        logo_x = SCREEN_WIDTH // 2 - self.title_image.get_width() // 2
        logo_y = SCREEN_HEIGHT // 2 - self.title_image.get_height()
        self.screen.blit(self.title_image, (logo_x, logo_y))

    def _draw_menu_text(self):
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
        self._draw_lives()
        self._draw_speed()
        pygame.display.flip()

    def game_over(self):
        self.state = 'game_over'
        pygame.mixer.music.stop()
        if self.player:
            self.player.state.stop_sounds()

        self.captured_surface = self.screen.copy()
        self.game_over_overlay_alpha = 0

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.state = 'menu'
                elif event.key == pygame.K_r:
                    self.load_game()

    def game_over_draw(self):
        if self.captured_surface:
            self.screen.blit(self.captured_surface, (0, 0))

        if self.game_over_overlay_alpha < 150:
            self.game_over_overlay_alpha += 1

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(self.game_over_overlay_alpha)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        font = pygame.font.Font(self.font_path, 50)
        text = font.render("게임 오버", True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(text, text_rect)

        small_font = pygame.font.Font(self.font_path, 30)
        menu_text = small_font.render("메뉴로 돌아가기 (Enter)", True, (255, 255, 255))
        retry_text = small_font.render("다시하기 (R)", True, (255, 255, 255))

        menu_x = SCREEN_WIDTH // 2 - menu_text.get_width() // 2
        menu_y = SCREEN_HEIGHT // 2
        retry_x = SCREEN_WIDTH // 2 - retry_text.get_width() // 2
        retry_y = menu_y + 50

        self.screen.blit(menu_text, (menu_x, menu_y))
        self.screen.blit(retry_text, (retry_x, retry_y))

        pygame.display.flip()


    def _draw_lives(self):
        font = pygame.font.Font(self.font_path, 20)
        text = font.render(f"Lives: {self.player.state.lives}", True, BLACK)
        self.screen.blit(text, (10, 10))

    def _draw_speed(self):
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

        self._reset_groups()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.load_level(level_file)
        self.player.state.stop_sounds()
        self.state = 'game'
        pygame.mixer.music.play(-1)
