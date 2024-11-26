# state.py
import pygame
from Platformer.src.settings import JUMPING_SOUND, RUNNING_SOUND


class PlayerState:
    def __init__(self):
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2000  # 무적 시간 (밀리초)
        self._initialize_sound()

    def _initialize_sound(self):
        """사운드 효과 초기화"""
        try:
            self.jump_sound = pygame.mixer.Sound(JUMPING_SOUND)
            self.running_sound = pygame.mixer.Sound(RUNNING_SOUND)
            self.is_running_sound_playing = False
        except pygame.error as e:
            print(f"사운드 로드 실패: {e}")

            # 더미 사운드 객체 생성
            class DummySound:
                def play(self, *args): pass

                def stop(self): pass

            self.jump_sound = DummySound()
            self.running_sound = DummySound()
            self.is_running_sound_playing = False

    def update_invincibility(self):
        """무적 상태 업데이트"""
        if self.invincible and pygame.time.get_ticks() - self.invincible_timer > self.invincible_duration:
            self.invincible = False

    def take_damage(self):
        """데미지를 입었을 때의 처리"""
        if not self.invincible:
            self.lives -= 1
            print(f"{self.lives} lives left")
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()

    def play_jump_sound(self):
        """점프 사운드 재생"""
        self.jump_sound.play()

    def update_running_sound(self, is_running):
        """달리기 사운드 상태 업데이트"""
        if is_running and not self.is_running_sound_playing:
            self.running_sound.play(-1)
            self.is_running_sound_playing = True
        elif not is_running and self.is_running_sound_playing:
            self.running_sound.stop()
            self.is_running_sound_playing = False

    def reset(self):
        """상태 초기화"""
        self.lives = 3
        self.invincible = False
        self.invincible_timer = 0

