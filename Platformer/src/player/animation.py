from Platformer.src.player.image_loader import *

class PlayerAnimation:
    def __init__(self):
        self.frame_count = 0
        self.frame_delay = 5

    def update(self, player, physics, movement):
        if physics.vel_y < 0:  # 점프 중
            player.image = (player.image_loader.get_image('right_jump')
                            if movement.facing == "right"
                            else player.image_loader.get_image('left_jump'))
        elif physics.vel_x != 0 and physics.on_ground:  # 달리는 중
            self._update_running_animation(player, physics, movement)
        else:  # 정지 상태
            self._update_standing_animation(player, movement)

        # 달리기 상태에 따른 애니메이션 속도 조절
        base_delay = 3 if movement.is_running else 5
        self.frame_delay = max(2, int(base_delay - abs(physics.vel_x) / 2))

    def _update_running_animation(self, player, physics, movement):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            if movement.facing == "right":
                current_image = player.image_loader.get_image('standing_right')
                run_image = player.image_loader.get_image('right_run')
                player.image = (run_image if player.image == current_image
                                else current_image)
            else:
                current_image = player.image_loader.get_image('standing_left')
                run_image = player.image_loader.get_image('left_run')
                player.image = (run_image if player.image == current_image
                                else current_image)

    def _update_standing_animation(self, player, movement):
        player.image = (player.image_loader.get_image('standing_right')
                        if movement.facing == "right"
                        else player.image_loader.get_image('standing_left'))


# player.py에서 프로퍼티 제거 (더 이상 필요하지 않음)
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game

        # 컴포넌트 초기화
        self.image_loader = PlayerImageLoader()
        self.collision_handler = PlayerCollisionHandler(game)
        self.physics = PlayerPhysics()
        self.movement = PlayerMovement()
        self.animation = PlayerAnimation()
        self.state = PlayerState()

        # 기본 이미지와 rect 설정
        self.image = self.image_loader.get_image('standing')
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH / 2
        self.rect.bottom = SCREEN_HEIGHT