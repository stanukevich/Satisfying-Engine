from typing import TYPE_CHECKING

from managers.manager import Manager


if TYPE_CHECKING:
    from entities.entity import Entity


class EntityManager(Manager):
    def __init__(self):
        self.entities = []

    def add(self, entity: "Entity"):
        self.entities.append(entity)

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt)  

    def draw(self, surface):
        for entity in self.entities:
            entity.draw(surface)