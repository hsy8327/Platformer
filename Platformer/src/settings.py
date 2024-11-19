import pygame

#화면설정
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "platformer_test"

#색상 정의
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

#캐릭터 설정
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = 17
GRAVITY = 1
MAX_FALL_SPEED = 10

#타일 설정
TILE_SIZE = 32

#assets 경로
FONT_PATH = "assets/fonts/Cafe24Ohsquare-v2.0.ttf"

CLOUD_PATH = "assets/cloud.png"
SCHOOL_IMG_PATH = "assets/school.png"
BACKGROUND_MUSIC_PATH = "assets/Storytelling Cartoon MusicComedy 06.mp3"
TITLE_IMG_PATH ="assets/title.png"

#PLAYER 관련
PLAYER_IMG = "assets/playerImage/right_mario.png"
PLAYER_IMG_RIGHT_RUN = "assets/playerImage/right_run.png"
PLAYER_IMG_LEFT_RUN = "assets/playerImage/left_run.png"
PLAYER_IMG_RIGHT_JUMP = "assets/playerImage/right_jump.png"
PLAYER_IMG_LEFT_JUMP = "assets/playerImage/left_jump.png"
PLAYER_IMG_STANDING_RIGHT = "assets/playerImage/right_mario.png"
PLAYER_IMG_STANDING_LEFT = "assets/playerImage/left_mario.png"

JUMPING_SOUND = "assets/playerSounds/jump-sound.mp3"
RUNNING_SOUND = "assets/playerSounds/running-sound.mp3"
