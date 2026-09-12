from typing import TYPE_CHECKING

from pygame import Vector2
import pygame.gfxdraw

from entities.entity import Entity
from entities.collisions import (
    check_ball_window_collision,
    resolve_ball_window_collision,
    check_ball_ball_collision,
    resolve_ball_ball_collision,
)
from entities.modifiers import (
    get_scaled_size,
    get_transparent_color
)


if TYPE_CHECKING:
    from world.map import Map
    from entities.ball import Ball


class Ball(Entity):
    def __init__(self, gravity, restitution, x, y, radius, color):
        super().__init__(gravity, restitution)

        self.position = Vector2(x, y)
        self.radius = radius
        self.color = color

    def update(self, dt):
        super().update(dt)
    
        self.position += self.velocity * dt

    def resize(self, scale):
        current_size = self.radius
        self.radius = get_scaled_size(current_size, scale)

    def transparency(self, factor):
        current_color = self.color
        self.color = get_transparent_color(current_color, factor)

    def process_window_collision(self, window):
        super().process_window_collision(window)

        width, height = window

        if check_ball_window_collision(width, height, self):
            resolve_ball_window_collision(width, height, self)

    def process_map_collision(self, game_map: "Map"):
        game_map.process_ball_collision(self)

    def process_entity_collision(self, entity):
        if isinstance(entity, Ball):
            if check_ball_ball_collision(self, entity):
                resolve_ball_ball_collision(self, entity)

    def draw(self, surface):
        x = int(self.position.x)
        y = int(self.position.y)
        r = int(self.radius)

        pygame.gfxdraw.aacircle(
            surface,
            x,
            y,
            r,
            self.color
        )

        pygame.gfxdraw.filled_circle(
            surface,
            x,
            y,
            r,
            self.color
        )     

    def draw_transformed(self, surface, point, factor = 1):
        x = int(point.x)
        y = int(point.y)
        current_radius = self.radius
        current_color = self.color
        new_radius = get_scaled_size(current_radius, factor)
        new_color = get_transparent_color(current_color, factor)

        pygame.gfxdraw.filled_circle(
            surface,
            int(x),
            int(y),
            new_radius,
            new_color
        )

    def get_position(self):
        return self.position

    def get_color(self):
        return self.color

    def set_color(self, new_color):
        self.color = new_color