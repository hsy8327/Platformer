import serial
import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_SPACE, K_LSHIFT

# 시리얼 포트 설정 (라즈베리 파이의 실제 포트 경로로 바꿀 것)
ser = serial.Serial('/dev/COM3', 9600, timeout=1)

pygame.init()

screen = pygame.display.set_mode((800, 600))
running = True

while running:
    if ser.in_waiting:
        try:
            # 아두이노로부터 데이터 읽기
            line = ser.readline().decode('utf-8').rstrip()
            x_value, button_jump, button_shift = map(int, line.split(','))

            # 사용자 입력 시뮬레이션
            keys = [0] * 256

            # 조이스틱 처리
            if x_value < 400:  # 임계값 아래면 왼쪽으로
                keys[K_LEFT] = 1
            elif x_value > 600:  # 임계값 위면 오른쪽으로
                keys[K_RIGHT] = 1

            # 점프 버튼 처리
            if button_jump:
                keys[K_SPACE] = 1

            # 쉬프트 버튼 처리 (달리기)
            if button_shift:
                keys[K_LSHIFT] = 1

            # 이 keys 배열을 파이게임에서 처리
            # 예컨대 player.handle_input(keys) et al.

        except ValueError:
            print("Reading error")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()