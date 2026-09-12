from typing import TYPE_CHECKING

from managers.entity_manager import EntityManager


if TYPE_CHECKING:
    from entities.ball import Ball


class Map(EntityManager):
    def process_ball_collision(self, ball: "Ball"):
        for wall in self.entities:
            wall.process_ball_collision(ball)