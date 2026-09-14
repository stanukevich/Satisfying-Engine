from typing import TYPE_CHECKING

from pygame import Vector2
import pygame.gfxdraw

from entities.entity import Entity
from entities.collisions import (
    CollisionType,
    check_ball_window_collision,
    resolve_ball_window_collision,
    check_ball_ball_collision,
    resolve_ball_ball_collision
)
from entities.modifiers import (
    get_scaled_size,
    get_transparent_color
)
from events.collision_event import CollisionEvent


if TYPE_CHECKING:
    from world.map import Map
    from entities.ball import Ball
    from events.event import Event


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

    def process_window_collision(self, window, events: list["Event"]):
        width, height = window

        if check_ball_window_collision(width, height, self):
            impact = resolve_ball_window_collision(width, height, self)

            if self.velocity.y != 0:
                events.append(
                    CollisionEvent(
                        CollisionType.ENTITY_WINDOW,
                        self,
                        None,
                        impact
                    )
                )

    def process_map_collision(self, game_map: "Map", events: list["Event"]):
        game_map.process_ball_collision(self, events)

    def process_entity_collision(self, entity, events: list["Event"]):
        if isinstance(entity, Ball):
            if check_ball_ball_collision(self, entity):
                impact = resolve_ball_ball_collision(self, entity)

                events.append(
                    CollisionEvent(
                        CollisionType.ENTITY_ENTITY,
                        self,
                        entity,
                        impact
                    )
                )

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