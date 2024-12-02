import pygame
import serial
import time
from pygame.locals import KEYDOWN, KEYUP
from Platformer.src.blocks.level_loader import LevelLoader
from Platformer.src.player.player import Player
from Platformer.src.settings import *


class Game:
   def __init__(self):
       pygame.init()
       pygame.mixer.init()
       self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
       pygame.display.set_caption("test")
       self.clock = pygame.time.Clock()
       self.running = True
       self.state = 'menu'


       self.all_sprites = pygame.sprite.Group()
       self.platforms = pygame.sprite.Group()
       self.ground = pygame.sprite.Group()
       self.breakable_blocks = pygame.sprite.Group()
       self.pathable_platforms = pygame.sprite.Group()
       self.spikes = pygame.sprite.Group()
       self.goal = pygame.sprite.Group()
       self.cutlets = pygame.sprite.Group()  # 커틀렛 그룹 추가


       self.player = Player(self)
       self.start_ticks = pygame.time.get_ticks()
       # 왕관 이미지 로드
       self.crown_image = pygame.image.load("assets/crown.png").convert_alpha()
       self.crown_rect = self.crown_image.get_rect(bottomright=(SCREEN_WIDTH - 10, SCREEN_HEIGHT - 40))  # 하단 오른쪽 위치


       self.cloud_image = pygame.image.load(CLOUD_PATH).convert_alpha()
       self.school_image = pygame.image.load(SCHOOL_IMG_PATH).convert_alpha()


       self.show_text = True
       self.text_timer = 0
       self.text_blink_interval = 500
       self.background_music = BACKGROUND_MUSIC_PATH
       self.current_level = 1


       self.font_path = FONT_PATH
       self.title_image = pygame.image.load(TITLE_IMG_PATH).convert_alpha()
       self.camera_offset = 0
       self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
       self.draw_fixed_background(self.background)
       self.game_over_surface = None


       self.game_over_overlay_alpha = 0
       self.captured_surface = None


       self.timer_font = pygame.font.Font(self.font_path, 30)  # 타이머 글꼴
       self.elapsed_time = 0
       self.clear_time = 0
       self.timer_visible = True  # 타이머 가시성 제어
       self.goal_proximity_threshold = 100  # 목표에 가까워지는 기준 거리


       self.clouds = []


       # 시리얼 통신 설정
       self.ser = serial.Serial('/dev/ttyUSB0', 9600)  # 시리얼 포트를 환경에 맞게 변경


       # 키 상태를 저장하는 변수
       self.key_states = {
           'left': False,
           'right': False,
           'jump': False,
           'run': False
       }


       for i in range(5):
           x = i * self.cloud_image.get_width()
           y = 50 if i % 2 == 0 else 100
           self.clouds.append(pygame.Rect(x, y, self.cloud_image.get_width(), self.cloud_image.get_height()))


   def load_game(self):
       self.state = 'game'
       self.current_level = 1
       self.all_sprites.empty()
       self.platforms.empty()
       self.ground.empty()
       self.breakable_blocks.empty()
       self.pathable_platforms.empty()
       self.spikes.empty()
       self.goal.empty()
       self.cutlets.empty()
       self.player = Player(self)
       self.all_sprites.add(self.player)
       self.load_level(f'levels/level{self.current_level}.json')
       if self.background_music:
           pygame.mixer.music.load(self.background_music)
           pygame.mixer.music.play(-1)  # 타이머 초기화
       self.start_ticks = pygame.time.get_ticks()
       self.elapsed_time = 0


   def load_level(self, level_file):
       self.all_sprites.empty()
       self.platforms.empty()
       self.ground.empty()
       self.breakable_blocks.empty()
       self.pathable_platforms.empty()
       self.spikes.empty()
       self.goal.empty()
       self.cutlets.empty()


       self.player = Player(self)
       self.all_sprites.add(self.player)


       level_loader = LevelLoader(self, level_file)
       level_loader.load_level()


       if self.background_music:
           pygame.mixer.music.load(self.background_music)
           pygame.mixer.music.play(-1)


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
           elif self.state == 'clear':
               self.clear_events()
               self.clear_draw()
           elif self.state == 'ranking':
               self.ranking_events()
               self.ranking_draw()


       pygame.quit()


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


       school_x = SCREEN_WIDTH - self.school_image.get_width() - 600
       school_y = SCREEN_HEIGHT - self.school_image.get_height() - 10
       surface.blit(self.school_image, (school_x, school_y))


   def menu_events(self):
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               self.running = False
           elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
               self.load_game()
           elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼 클릭 이벤트
               if event.button == 1:  # 왼쪽 버튼 클릭
                   if self.crown_rect.collidepoint(event.pos):  # 왕관 클릭 확인
                       self.state = 'ranking'  # 상태를 'ranking'으로 변경


   def menu_draw(self):
       self.screen.blit(self.background, (0, 0))
       # 왕관 이미지를 메뉴화면에 그리기
       self.screen.blit(self.crown_image, self.crown_rect)
       pygame.display.flip()


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






   def events(self):
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               self.running = False
       self.read_arduino_data()


   def update(self):
       if self.state == 'game':
           current_ticks = pygame.time.get_ticks()
           self.elapsed_time = current_ticks - self.start_ticks


           # 목표와의 거리 확인
           self.check_goal_proximity()


           self.update_clouds()
           self.all_sprites.update()
           self.update_camera()


   def draw(self):
       self.screen.blit(self.background, (0, 0))
       self.draw_clouds()
       for sprite in self.all_sprites:
           self.screen.blit(sprite.image, (sprite.rect.x + self.camera_offset, sprite.rect.y))


       if self.state != 'clear' and self.timer_visible:
           self.draw_timer()


       self.draw_lives()
       pygame.display.flip()


   def draw_lives(self):
       font = pygame.font.Font(self.font_path, 30)
       text = font.render(f"Lives: {self.player.state.lives}", True, BLACK)
       self.screen.blit(text, (10, 10))


   def next_level(self):
       self.clear_level()


   def clear_level(self):
       """클리어 상태로 전환하면서 타이머를 멈추고 값을 저장."""
       pygame.display.flip()  # 화면 캡처 전 마지막으로 업데이트


       self.state = 'clear'
       self.clear_time = self.elapsed_time  # 클리어 시점의 시간 저장
       pygame.mixer.music.stop()
       if self.player:
           self.player.state.stop_sounds()


       # 현재 화면 캡처
       self.captured_surface = self.screen.copy()


   def clear_events(self):
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               self.running = False
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_h:  # 홈 메뉴로 돌아가기
                   self.state = 'menu'
               elif event.key == pygame.K_c:  # 다음 스테이지로 도전하기
                   self.load_next_level()
               elif event.key == pygame.K_s:  # S 키 눌렀을 때 점수 저장
                   self.save_score()


   def save_score(self):
       """랭킹 저장 함수"""
       with open("rankings.txt", "a") as file:
           total_seconds = self.clear_time // 1000
           milliseconds = self.clear_time % 1000
           formatted_time = f"{total_seconds // 60:02}:{total_seconds % 60:02}.{milliseconds:03}"
           file.write(f"Score: {formatted_time}\n")
       print("Score saved!")


   def clear_draw(self):
       if self.captured_surface:
           self.screen.blit(self.captured_surface, (0, 0))


       # 클리어 메시지
       big_font = pygame.font.Font(self.font_path, 50)
       clear_text = big_font.render("클리어!", True, (255, 255, 255))
       clear_x = SCREEN_WIDTH // 2 - clear_text.get_width() // 2
       clear_y = SCREEN_HEIGHT // 3 - clear_text.get_height() // 2
       self.screen.blit(clear_text, (clear_x, clear_y))


       # 클리어 시간 표시
       total_seconds = self.clear_time // 1000
       milliseconds = self.clear_time % 1000
       formatted_time = f"{total_seconds // 60:02}:{total_seconds % 60:02}.{milliseconds:03}"
       time_surface = self.timer_font.render(f"기록: {formatted_time}", True, (255, 255, 255))
       time_x = SCREEN_WIDTH // 2 - time_surface.get_width() // 2
       time_y = clear_y + 60


       self.screen.blit(time_surface, (time_x, time_y))


       # 홈 및 도전 버튼
       small_font = pygame.font.Font(self.font_path, 30)
       home_text = small_font.render("홈으로 돌아가기 (H)", True, (255, 255, 255))
       home_x = SCREEN_WIDTH // 2 - home_text.get_width() // 2
       home_y = time_y + 100
       self.screen.blit(home_text, (home_x, home_y))
       self.home_button_rect = home_text.get_rect(center=(SCREEN_WIDTH // 2, home_y))


       challenge_text = small_font.render("도전하기 (C)", True, (255, 255, 255))
       challenge_x = SCREEN_WIDTH // 2 - challenge_text.get_width() // 2
       challenge_y = home_y + 50
       self.screen.blit(challenge_text, (challenge_x, challenge_y))


       save_text = small_font.render("저장하기 (S)", True, (255, 255, 255))
       save_x = SCREEN_WIDTH // 2 - save_text.get_width() // 2
       save_y = challenge_y + 50
       self.screen.blit(save_text, (save_x, save_y))


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


   def load_next_level(self):
       self.current_level += 1
       level_file = f'levels/level{self.current_level}.json'
       try:
           self.load_level(level_file)
           print(f"레벨 {self.current_level} 시작")
           self.state = 'game'
           self.start_ticks = pygame.time.get_ticks()
           self.elapsed_time = 0
       except FileNotFoundError:
           print("모든 레벨을 완료했습니다. 메인 메뉴로 돌아갑니다.")
           self.state = 'menu'
       except Exception as e:
           print(f"레벨 로드 중 에러: {e}")


   def draw_timer(self):
       total_seconds = self.elapsed_time // 1000
       milliseconds = self.elapsed_time % 1000
       formatted_time = f"{total_seconds // 60:02}:{total_seconds % 60:02}.{milliseconds:03}"
       timer_surface = self.timer_font.render(formatted_time, True, BLACK)
       timer_rect = timer_surface.get_rect(topright=(SCREEN_WIDTH - 10, 10))
       self.screen.blit(timer_surface, timer_rect)


   def update_clouds(self):
       for cloud in self.clouds:
           if self.player.movement.facing == "right" and abs(self.player.physics.vel_x) > 0:
               cloud.x -= 2
           elif self.player.movement.facing == "left" and abs(self.player.physics.vel_x) > 0:
               cloud.x += 2


           if cloud.right < 0:
               cloud.x = SCREEN_WIDTH
           elif cloud.left > SCREEN_WIDTH:
               cloud.x = -cloud.width


   def draw_clouds(self):
       for cloud in self.clouds:
           self.screen.blit(self.cloud_image, (cloud.x, cloud.y))


   def check_goal_proximity(self):
       """플레이어가 목표에 가까워질 때 타이머를 숨깁니다."""
       for goal in self.goal:
           distance = abs(self.player.rect.centerx - goal.rect.centerx)
           if distance < self.goal_proximity_threshold:
               self.timer_visible = False
               break  # 목표가 여러 개여도 하나만 감지하면 됨
           else:
               self.timer_visible = True


   def ranking_draw(self):
       self.screen.blit(self.background, (0, 0))  # 배경 그리기
       header_font = pygame.font.Font(self.font_path, 50)
       header_text = header_font.render("대학생 랭킹", True, (255, 255, 255))


       # 헤더 텍스트 위치
       header_x = SCREEN_WIDTH // 2 - header_text.get_width() // 2
       header_y = SCREEN_HEIGHT // 4 - header_text.get_height() // 2


       self.screen.blit(header_text, (header_x, header_y))


       # 여기에 랭킹 내용을 추가로 그릴 수 있음
       ranking_font = pygame.font.Font(self.font_path, 30)
       rankings = ["1. 플레이어1 - 150점", "2. 플레이어2 - 120점", "3. 플레이어3 - 100점"]  # 샘플 랭킹


       for i, ranking in enumerate(rankings):
           ranking_text = ranking_font.render(ranking, True, (255, 255, 255))
           self.screen.blit(ranking_text,
                            (SCREEN_WIDTH // 2 - ranking_text.get_width() // 2, SCREEN_HEIGHT // 4 + 100 + i * 40))


       # 홈으로 돌아가기 버튼
       home_button_text = ranking_font.render("홈으로 돌아가기 (H)", True, (255, 255, 255))
       home_button_rect = home_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
       self.screen.blit(home_button_text, home_button_rect)


       pygame.display.flip()


   def ranking_events(self):
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               self.running = False
           elif event.type == pygame.KEYDOWN:
               if event.key == pygame.K_h:  # 홈으로 돌아가기
                   self.state = 'menu'
           elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼 클릭 이벤트
               if event.button == 1:  # 왼쪽 버튼 클릭
                   # 홈 버튼 클릭 확인
                   if self.home_button_rect.collidepoint(event.pos):
                       self.state = 'menu'


   def read_arduino_data(self):
       try:
           if self.ser.in_waiting > 0:
               data = self.ser.readline().decode('utf-8').strip()
               self.process_arduino_data(data)  # 데이터를 처리하는 메서드
       except serial.SerialException as e:
           print(f"시리얼 통신 오류: {e}")
       except OSError as e:
           print(f"I/O 오류: {e}")
       except Exception as e:
           print(f"기타 오류: {e}")




   def process_arduino_data(self, data):
       try:
           joystick_x, button1, button2 = map(int, data.split(','))  # 전달받을 데이터에 따라 조정


           # 조이스틱을 왼쪽으로 움직일 때
           if joystick_x < 400:  # 임계값을 조정 가능
               if not self.key_states['left']:
                   pygame.event.post(pygame.event.Event(KEYDOWN, {'key': pygame.K_LEFT}))
                   self.key_states['left'] = True
               if self.key_states['right']:
                   pygame.event.post(pygame.event.Event(KEYUP, {'key': pygame.K_RIGHT}))
                   self.key_states['right'] = False


           # 조이스틱을 오른쪽으로 움직일 때
           elif joystick_x > 600:  # 임계값을 조정 가능
               if not self.key_states['right']:
                   pygame.event.post(pygame.event.Event(KEYDOWN, {'key': pygame.K_RIGHT}))
                   self.key_states['right'] = True
               if self.key_states['left']:
                   pygame.event.post(pygame.event.Event(KEYUP, {'key': pygame.K_LEFT}))
                   self.key_states['left'] = False


           # 조이스틱의 중앙에 있을 때
           else:
               if self.key_states['left']:
                   pygame.event.post(pygame.event.Event(KEYUP, {'key': pygame.K_LEFT}))
                   self.key_states['left'] = False
               if self.key_states['right']:
                   pygame.event.post(pygame.event.Event(KEYUP, {'key': pygame.K_RIGHT}))
                   self.key_states['right'] = False


           # 버튼 입력 처리
           if button1:  # 예: button1이 스페이스바 역할
               if not self.key_states['jump']:
                   pygame.event.post(pygame.event.Event(KEYDOWN, {'key': pygame.K_SPACE}))
                   self.key_states['jump'] = True
           else:
               if self.key_states['jump']:
                   pygame.event.post(pygame.event.Event(KEYUP, {'key': pygame.K_SPACE}))
                   self.key_states['jump'] = False


           if button2:  # 예: button2가 시프트 역할
               if not self.key_states['run']:
                   pygame.event.post(pygame.event.Event(KEYDOWN, {'key': pygame.K_LSHIFT}))
                   self.key_states['run'] = True
           else:
               if self.key_states['run']:
                   pygame.event.post(pygame.event.Event(KEYUP, {'key': pygame.K_LSHIFT}))
                   self.key_states['run'] = False


       except ValueError as e:
           print("데이터 파싱 오류:", e)


if __name__ == "__main__":
   game = Game()
   game.run()


