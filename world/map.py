from managers.entity_manager import EntityManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.ball import Ball

class Map(EntityManager):
    def process_ball_collision(self, ball: "Ball"):
        for wall in self.entities:
            wall.process_ball_collision(ball)