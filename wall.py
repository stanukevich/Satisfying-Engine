import pygame

class Wall:
    def __init__(self, points, thickness, color):
        self.points = [
            pygame.Vector2(point) 
            for point in points
        ]
        self.thickness = thickness
        self.color = color

    def draw(self, surface):
        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i + 1]
            pygame.draw.aaline(
                surface,
                self.color,
                start,
                end
            )