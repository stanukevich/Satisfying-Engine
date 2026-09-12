from typing import TYPE_CHECKING

from pygame import Vector2


if TYPE_CHECKING:
    from world.map import Map
    from effects.effect import Effect


class Entity:
    def __init__(self, gravity, restitution):
        self.velocity = Vector2(0, 0)
        self.gravity = gravity
        self.restitution = restitution
        # self.effects = []

    def update(self, dt):
        self.velocity.y += self.gravity * dt

    def resize(self, scale):
        pass

    def transparency(self, factor):
        pass

    def process_window_collision(self, window):
        pass

    def process_map_collision(self, game_map: "Map"):
        pass

    def process_entity_collision(self, entity: "Entity"):
        pass

    def draw(self, surface):
        pass

    def draw_transformed(self, surface, factor, point):
        pass

    # def draw_effects(self, surface):
    #     for effect in self.effects:
    #         effect.draw(surface, self)

    def get_position(self):
        pass

    # def add_effect(self, effect: "Effect"):
        self.effects.append(effect)