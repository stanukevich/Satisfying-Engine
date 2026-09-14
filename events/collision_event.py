from typing import TYPE_CHECKING

from config import MAX_IMPACT
from events.event import Event


if TYPE_CHECKING:
    from entities.entity import Entity
    from entities.collisions import CollisionType


class CollisionEvent(Event):
    def __init__(self, type: "CollisionType", entity_a: "Entity", entity_b: "Entity", impact = 0):
        super().__init__(type)

        self.entity_a = entity_a
        self.entity_b = entity_b
        self.impact = min(impact / MAX_IMPACT, 1.0)

    def get_impact(self):
        return self.impact