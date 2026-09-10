from pygame import Vector2
from copy import deepcopy

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world.map import Map
    from effects.effect import Effect

class Entity:
    def __init__(self, gravity, restitution):
        self.velocity = Vector2(0, 0)
        self.gravity = gravity
        self.restitution = restitution
        self.effects = []

    # def copy(self):
    #     return deepcopy(self)

    def update(self, dt):
        self.velocity.y += self.gravity * dt

    def resize(self, scale):
        pass

    def transparency(self, factor):
        pass

    def draw(self, surface):
        pass

    def process_window_collision(self, window):
        pass

    def process_map_collision(self, game_map: "Map"):
        pass

    def process_entity_collision(self, entity: "Entity"):
        pass

    def add_effect(self, effect: "Effect"):
        self.effects.append(effect)

    def draw_effects(self, surface):
        for effect in self.effects:
            effect.draw(surface, self)

    def draw_transformed(self, surface, factor, point):
        pass

    def get_position(self):
        pass