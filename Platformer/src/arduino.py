import pygame
import serial


class ArduinoController:
    def __init__(self, port='/dev/ttyUSB0'):
        try:
            self.serial = serial.Serial(port, 9600)
        except serial.SerialException:
            try:
                self.serial = serial.Serial('/dev/ttyACM0', 9600)
            except serial.SerialException:
                print("아두이노 연결 실패. 키보드 입력만 사용합니다.")
                self.serial = None

        self.x_value = 512
        self.button1 = 0
        self.button2 = 0

    def update(self):
        if self.serial and self.serial.in_waiting:
            try:
                data = self.serial.readline().decode().strip().split(',')
                if len(data) == 3:
                    self.x_value = int(data[0])
                    self.button1 = int(data[1])
                    self.button2 = int(data[2])
            except:
                pass

    def get_input_state(self, keys):
        if self.serial:
            self.update()
            return (
                self.x_value < 400 or keys[pygame.K_LEFT],
                self.x_value > 600 or keys[pygame.K_RIGHT],
                bool(self.button1) or keys[pygame.K_SPACE],
                bool(self.button2) or keys[pygame.K_LSHIFT]
            )
        return (
            keys[pygame.K_LEFT],
            keys[pygame.K_RIGHT],
            keys[pygame.K_SPACE],
            keys[pygame.K_LSHIFT]
        )