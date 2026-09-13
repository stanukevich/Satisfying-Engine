from typing import TYPE_CHECKING

from pygame import draw, Vector2

from entities.entity import Entity
from entities.collisions import (
    CollisionType,
    check_ball_segment_collision, 
    resolve_ball_segment_collision
)
from events.collision_event import CollisionEvent

if TYPE_CHECKING:
    from entities.ball import Ball
    from events.event import Event


class Wall(Entity):
    def __init__(self, points, thickness, color):
        self.points = [
            Vector2(point) 
            for point in points
        ]
        self.thickness = thickness
        self.color = color

    def draw(self, surface):
        for i in range(len(self.points) - 1):
            start = self.points[i]
            end = self.points[i + 1]
            draw.aaline(
                surface,
                self.color,
                start,
                end
            )

    def process_ball_collision(self, ball: "Ball", events: list["Event"]):
        points = self.points
        thickness = self.thickness

        for i in range(len(points) - 1):
            start = points[i]
            end = points[i + 1]
            if(check_ball_segment_collision(start, end, thickness, ball)):
                resolve_ball_segment_collision(start, end, thickness, ball)

                events.append(
                    CollisionEvent(
                        CollisionType.ENTITY_WALL,
                        self,
                        ball
                    )
                )