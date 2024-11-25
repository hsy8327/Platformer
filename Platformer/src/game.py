import pygame
from .player import Player
from .settings import *
from Platformer.src.blocks.level_loader import LevelLoader


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Platformer Test")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'menu'

        # 스프라이트 그룹
        self.all_sprites = pygame.sprite.Group()
        self.f_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.ground = pygame.sprite.Group()
        self.breakable_blocks = pygame.sprite.Group()
        self.pathable_platforms = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.goal = pygame.sprite.Group()
        self.player = None

        # 이미지 및 폰트 로드
        self.cloud_image = pygame.image.load(CLOUD_PATH).convert_alpha()
        self.school_image = pygame.image.load(SCHOOL_IMG_PATH).convert_alpha()
        self.font_path = FONT_PATH
        self.title_image = pygame.image.load(TITLE_IMG_PATH).convert_alpha()
        self.background_music = BACKGROUND_MUSIC_PATH

        # 초기 값 설정
        self.current_level = 0
        self.camera_offset = 0
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.draw_fixed_background(self.background)

        # 텍스트 깜박임 관련 설정
        self.show_text = True
        self.text_timer = 0
        self.text_blink_interval = 500

        # 게임 시간 관련 변수
        self.start_ticks = None

        self.clear_time = 0  # 클리어 시간 기본값 설정

    def load_game(self):
        self.state = 'game'
        self.current_level = 1  # 항상 첫 번째 레벨로 초기화
        self.all_sprites.empty()
        self.f_sprites.empty()
        self.platforms.empty()
        self.ground.empty()
        self.breakable_blocks.empty()
        self.pathable_platforms.empty()
        self.spikes.empty()
        self.goal.empty()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.load_level(f'levels/level{self.current_level}.json')
        self.start_ticks = pygame.time.get_ticks()

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
            elif self.state == 'game_over':
                self.game_over_events()
                self.game_over_draw()
            elif self.state == 'level_clear':
                self.level_clear_events()
                self.level_clear_draw()
        pygame.quit()

    def stop_sounds(self):
        pygame.mixer.music.stop()
        if self.player:
            self.player.running_sound.stop()

    def update_camera(self):
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

        surface.blit(self.cloud_image, (100, 50))
        surface.blit(self.cloud_image, (400, 100))

        school_x = SCREEN_WIDTH - self.school_image.get_width() - 600
        school_y = SCREEN_HEIGHT - self.school_image.get_height() - 23
        surface.blit(self.school_image, (school_x, school_y))

    def menu_draw(self):
        self.screen.blit(self.background, (0, 0))

        # 로고 그리기
        logo_x = SCREEN_WIDTH // 2 - self.title_image.get_width() // 2
        logo_y = SCREEN_HEIGHT // 2 - self.title_image.get_height()
        self.screen.blit(self.title_image, (logo_x, logo_y))

        # 시작하기 버튼 텍스트 표시 위치
        font = pygame.font.Font(self.font_path, 40)
        start_text = font.render("시작하기", True, WHITE)
        text_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2))

        # 현재 시간 확인
        current_time = pygame.time.get_ticks()
        if current_time - self.text_timer > self.text_blink_interval:
            self.show_text = not self.show_text
            self.text_timer = current_time

        # 텍스트 깜박임 처리
        if self.show_text:
            self.screen.blit(start_text, text_rect)

        pygame.display.flip()

    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 200 // 2, SCREEN_HEIGHT // 1.2 - 50 // 2),
                                                (200, 50))

                if start_button_rect.collidepoint(mouse_pos):
                    self.load_game()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        self.f_sprites.update()
        self.update_camera()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, (sprite.rect.x + self.camera_offset, sprite.rect.y))
        for f in self.f_sprites:
            self.screen.blit(f.image, (f.rect.x + self.camera_offset, f.rect.y))

        self.draw_time()
        self.draw_lives()
        pygame.display.flip()

    def draw_time(self):
        elapsed_seconds = (pygame.time.get_ticks() - self.start_ticks) // 1000
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        time_string = f"{minutes:02}:{seconds:02}"
        font = pygame.font.Font(self.font_path, 20)
        text = font.render(time_string, True, BLACK)
        text_x = SCREEN_WIDTH - text.get_width() - 10
        text_y = 10
        self.screen.blit(text, (text_x, text_y))

    def draw_lives(self):
        font = pygame.font.Font(self.font_path, 20)
        text = font.render(f"Lives: {self.player.lives}", True, BLACK)
        self.screen.blit(text, (10, 10))

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'menu'
                pygame.mixer.music.stop()

    def game_over_draw(self):
        game_over_screen = self.screen.copy()
        fade_alpha = 0
        fade_step = 5
        self.stop_sounds()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = 'menu'
                    return

            self.screen.blit(game_over_screen, (0, 0))
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(fade_alpha)
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.Font(self.font_path, 60)
            text = font.render("Game Over", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(text, text_rect)

            current_time = pygame.time.get_ticks()
            if current_time - self.text_timer > self.text_blink_interval:
                self.show_text = not self.show_text
                self.text_timer = current_time

            if self.show_text:
                font = pygame.font.Font(self.font_path, 30)
                sub_text = font.render("Press Enter to return to menu", True, WHITE)
                sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(sub_text, sub_text_rect)

            pygame.display.flip()
            fade_alpha = min(255, fade_alpha + fade_step)
            pygame.time.delay(30)

    def level_clear_draw(self):
        self.screen.blit(self.background, (0, 0))
        font = pygame.font.Font(self.font_path, 60)

        # "클리어!" 메시지 표시
        text = font.render("클리어!", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(self.font_path, 30)

        # 클리어 시간 표시
        clear_seconds = self.clear_time // 1000
        clear_minutes = clear_seconds // 60
        clear_seconds %= 60
        clear_time_string = f"클리어 시간: {clear_minutes:02}:{clear_seconds:02}"
        clear_time_text = font.render(clear_time_string, True, WHITE)
        clear_time_rect = clear_time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(clear_time_text, clear_time_rect)

        # "다음 스테이지에 도전하시겠습니까?" 메시지 표시
        sub_text = font.render("다음 스테이지에 도전하시겠습니까?", True, WHITE)
        sub_text_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(sub_text, sub_text_rect)

        # 버튼 텍스트
        home_text = font.render("홈으로 돌아가기", True, WHITE)
        challenge_text = font.render("다음 스테이지", True, WHITE)

        # 버튼 위치 계산
        button_width = 200
        button_height = 50
        home_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width - 10, SCREEN_HEIGHT // 2 + 50),
                                       (button_width, button_height))
        challenge_button_rect = pygame.Rect((SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 50),
                                            (button_width, button_height))

        # 검정 배경 없이 버튼 텍스트만 표시
        home_text_rect = home_text.get_rect(center=home_button_rect.center)
        challenge_text_rect = challenge_text.get_rect(center=challenge_button_rect.center)
        self.screen.blit(home_text, home_text_rect)
        self.screen.blit(challenge_text, challenge_text_rect)

        pygame.display.flip()

    def level_clear_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # 여기의 버튼 위치와 level_clear_draw의 버튼 위치가 동일해야 합니다.
                home_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 200 - 10, SCREEN_HEIGHT // 2 + 50), (200, 50))
                challenge_button_rect = pygame.Rect((SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 50), (200, 50))
                if home_button_rect.collidepoint(mouse_pos):
                    self.state = 'menu'
                elif challenge_button_rect.collidepoint(mouse_pos):
                    self.load_next_level()
    def load_next_level(self):
        self.current_level += 1
        level_file = f'levels/level{self.current_level}.json'
        try:
            with open(level_file, 'r'):
                self.state = 'game'
                self.all_sprites.empty()
                self.f_sprites.empty()
                self.platforms.empty()
                self.ground.empty()
                self.breakable_blocks.empty()
                self.pathable_platforms.empty()
                self.spikes.empty()
                self.goal.empty()
                self.player = Player(self)
                self.all_sprites.add(self.player)
                self.load_level(level_file)
                self.start_ticks = pygame.time.get_ticks()
                pygame.mixer.music.play(-1)
        except FileNotFoundError:
            self.state = 'menu'  # 레벨이 없을 경우 메인 화면으로 돌아갑니다