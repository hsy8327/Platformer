import json
import pygame

class BackgroundLoader:
    def __init__(self, game, background_file):
        self.game = game
        self.elements = []
        self.gradient = None

        # JSON 파일 읽기
        with open(background_file, 'r') as f:
            data = json.load(f)

        # 배경 그라디언트 정보 저장
        if "gradient" in data["background"]:
            self.gradient = data["background"]["gradient"]

        # 구름 및 빌딩 이미지 로드 및 위치 지정
        for element in data.get("clouds", []):
            image = pygame.image.load(element["image_path"]).convert_alpha()
            self.elements.append({
                "image": image,
                "x": element["x"] * 32,
                "y": element["y"] * 32,
                "parallax": element.get("parallax", 1.0)
            })

        for building in data.get("buildings", []):
            image = pygame.image.load(building["image_path"]).convert_alpha()
            self.elements.append({
                "image": image,
                "x": building["x"] * 32,
                "y": building["y"] * 32,
                "parallax": building.get("parallax", 1.0)
            })

    def draw(self, screen, camera_offset):
        # 배경 그라디언트 그리기
        if self.gradient:
            start_color = self.gradient["start_color"]
            end_color = self.gradient["end_color"]
            for y in range(self.game.screen.get_height()):
                blend_ratio = y / self.game.screen.get_height()
                blended_color = (
                    int(start_color[0] + (end_color[0] - start_color[0]) * blend_ratio),
                    int(start_color[1] + (end_color[1] - start_color[1]) * blend_ratio),
                    int(start_color[2] + (end_color[2] - start_color[2]) * blend_ratio),
                )
                pygame.draw.line(screen, blended_color, (0, y), (self.game.screen.get_width(), y))

        # 배경 요소 그리기 (Parallax 효과 적용)
        for element in self.elements:
            adjusted_x = element["x"] + camera_offset * element["parallax"]
            screen.blit(element["image"], (adjusted_x, element["y"]))
