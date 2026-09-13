from typing import TYPE_CHECKING

from managers.manager import Manager


if TYPE_CHECKING:
    from entities.entity import Entity
    from effects.effect import Effect


class EffectManager(Manager):
    def __init__(self):
        self.effects = {}

    def add(self, entity: "Entity", effect: "Effect"):
        if entity not in self.effects:
            self.effects[entity] = []

        self.effects[entity].append(effect)

    def update(self, dt):
        for entity, effects in self.effects.items():
            for effect in effects:
                effect.update(dt, entity)

    def draw(self, surface):
        for entity, effects in self.effects.items():
            for effect in effects:
                effect.draw(surface, entity)

    def get_entities(self):
        return self.effects

    def clear(self):
        self.effects.clear()