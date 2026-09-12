from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from entities.entity import Entity


class Effect:
    def __init__(self, size):
        self.size = size

    def update(self, dt, entity: "Entity"):
        pass
        
    def draw(self, surface, entity: "Entity"):
        pass