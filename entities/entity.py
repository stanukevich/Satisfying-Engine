from typing import TYPE_CHECKING

from pygame import Vector2


if TYPE_CHECKING:
    from world.map import Map
    from events.event import Event


class Entity:
    def __init__(self, gravity, restitution):
        self.velocity = Vector2(0, 0)
        self.gravity = gravity
        self.restitution = restitution

    def update(self, dt):
        self.velocity.y += self.gravity * dt

    def resize(self, scale):
        pass

    def transparency(self, factor):
        pass

    def process_window_collision(self, window, events: list["Event"]):
        pass

    def process_map_collision(self, game_map: "Map", events: list["Event"]):
        pass

    def process_entity_collision(self, entity: "Entity", events: list["Event"]):
        pass

    def draw(self, surface):
        pass

    def draw_transformed(self, surface, factor, point):
        pass

    def get_position(self):
        pass

    def get_color(self):
        pass

    def set_color(self, new_color):
        pass