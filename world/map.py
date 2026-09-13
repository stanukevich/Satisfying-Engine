from typing import TYPE_CHECKING

from managers.entity_manager import EntityManager


if TYPE_CHECKING:
    from entities.ball import Ball
    from events.event import Event


class Map(EntityManager):
    def process_ball_collision(self, ball: "Ball", events: list["Event"]):
        for wall in self.entities:
            wall.process_ball_collision(ball, events)