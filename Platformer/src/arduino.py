import time

import pygame
import serial
import serial.tools.list_ports


def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())

    # 더 많은 식별자 추가
    arduino_identifiers = [
        'Arduino',
        'CH340',
        'USB Serial',
        'USB-Serial',
        'USB2.0-Serial',
        'ttyUSB',
        'ttyACM'
    ]

    for p in ports:
        # description과 hwid 모두 확인
        if any(id in p.description or id in p.hwid for id in arduino_identifiers):
            return p.device

    print("사용 가능한 포트:", [p.device for p in ports])
    return None  # 기본값 제거, 연결되지 않았을 때 None 반환


class ArduinoController:
    def __init__(self, baudrate=115200):
        """아두이노 컨트롤러 초기화"""
        self.arduino = None
        self.last_input_state = {}
        self.connected = False
        self.DEADZONE = 50  # 데드존 값 설정

        # 아두이노 포트 찾기 및 연결
        self.connect_to_arduino(baudrate)

    def connect_to_arduino(self, baudrate):
        port = find_arduino_port()
        if port:
            try:
                self.arduino = serial.Serial(port, baudrate, timeout=0.01)
                print(f"아두이노가 {port}에 연결되었습니다.")
                self.connected = True
                # 아두이노 재설정 대기
                time.sleep(2)
                # 버퍼 비우기
                self.arduino.flushInput()
            except serial.SerialException as e:
                print(f"아두이노 연결 오류: {e}")
                print("키보드 모드로 전환합니다.")
        else:
            print("아두이노를 찾을 수 없습니다. 키보드 모드로 전환합니다.")

    def get_input_state(self):
        if not self.connected or not self.arduino:
            return self.last_input_state or {}

        try:
            if self.arduino.in_waiting > 0:
                data = self.arduino.readline().strip().decode('utf-8').split(',')
                if len(data) == 6:
                    x_axis = int(data[0])
                    button1 = bool(int(data[1]))
                    button2 = bool(int(data[2]))
                    flex1 = int(data[3])
                    # flex2 = int(data[4])
                    # mic = int(data[5])

                    # 중앙값을 기준으로 데드존 적용
                    center = 512
                    x_normalized = x_axis if abs(x_axis - center) >= self.DEADZONE else center

                    self.last_input_state = {
                        pygame.K_LEFT: x_normalized < (center - self.DEADZONE) or (flex1 > 200 and flex1 <= 600),
                        pygame.K_RIGHT: x_normalized > (center + self.DEADZONE), # or (flex2 > 200 and flex2 <= 600),
                        # pygame.K_SPACE: mic > 0,
                        pygame.K_UP: button1,
                        pygame.K_LSHIFT: flex1 > 600 ,# or flex2 > 600,  # shift + 왼쪽 화살표
                        pygame.K_RSHIFT: button2,  # shift + 오른쪽 화살표
                    }

            return self.last_input_state or {}

        except Exception as e:
            print(f"Error: {e}")
            return self.last_input_state or {}
    def reconnect(self):
        """아두이노 재연결 시도"""
        if not self.connected:
            port = find_arduino_port()
            if port:
                try:
                    if self.arduino:
                        self.arduino.close()
                    self.arduino = serial.Serial(port, 2000000, timeout=0.01)  # 속도 일관성 유지
                    self.connected = True
                    print(f"아두이노 재연결 성공: {port}")
                    time.sleep(2)
                    self.arduino.flushInput()
                except serial.SerialException as e:
                    print(f"아두이노 재연결 실패: {e}")

    def close(self):
        """시리얼 연결 종료"""
        if self.arduino:
            try:
                self.arduino.close()
                self.connected = False
                print("아두이노 연결이 종료되었습니다.")
            except serial.SerialException as e:
                print(f"아두이노 연결 종료 오류: {e}")

    def __del__(self):
        """소멸자에서 연결 종료"""
        self.close()

