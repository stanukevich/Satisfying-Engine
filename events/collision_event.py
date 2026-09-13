from typing import TYPE_CHECKING

from events.event import Event


if TYPE_CHECKING:
    from entities.entity import Entity
    from entities.collisions import CollisionType


class CollisionEvent(Event):
    def __init__(self, type: "CollisionType", entity_a: "Entity", entity_b: "Entity", impulse = 0):
        super().__init__(type)

        self.entity_a = entity_a
        self.entity_b = entity_b
        self.impulse = impulse