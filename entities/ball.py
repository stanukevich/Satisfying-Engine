from pygame import Vector2
import pygame.gfxdraw
from entities.entity import Entity
from engine import (
    check_ball_window_collision,
    resolve_ball_window_collision,
    check_ball_ball_collision,
    resolve_ball_ball_collision,
)

from entities.modifiers import (
    get_scaled_size,
    get_transparent_color
)

from typing import TYPE_CHECKING

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
        super().resize(scale)

        current_size = self.radius
        self.radius = get_scaled_size(current_size, scale)

    def transparency(self, factor):
        super().transparency(factor)

        current_color = self.color
        self.color = get_transparent_color(current_color, factor)

    def draw(self, surface):
        super().draw(surface)

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

    def process_window_collision(self, window):
        super().process_window_collision(window)

        width, height = window

        if check_ball_window_collision(width, height, self):
            resolve_ball_window_collision(width, height, self)

    def process_map_collision(self, game_map: "Map"):
        super().process_map_collision(game_map)

        game_map.process_ball_collision(self)

    def process_entity_collision(self, entity):
        super().process_entity_collision(entity)

        if isinstance(entity, Ball):
            if check_ball_ball_collision(self, entity):
                resolve_ball_ball_collision(self, entity) 

    def get_position(self):
        super().get_position()

        return self.position

    def draw_transformed(self, surface, factor, point):
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

    # def __init__(self, x, y, radius, ball_colors, collision_sounds, collision_effect_duration, restitution, gravity, trail_size):
    #     self.position = pygame.Vector2(x, y)
    #     self.radius = radius
    #     self.color = random.choice(ball_colors)
    #     self.velocity = pygame.Vector2(0, 0)
    #     self.restitution = restitution
    #     self.gravity = gravity

    #     self.trail_size = trail_size
    #     self.trail = []

    #     self.is_collision = False
    #     self.collision_sounds = collision_sounds
    #     self.collision_effect_duration = collision_effect_duration
    #     self.collision_effect = 0

    # # UPDATE

    # def update_trail(self):
    #     self.trail.append(self.position.copy())
    #     if len(self.trail) > self.trail_size:
    #         self.trail.pop(0)

    # def update(self, dt):
    #     if self.is_collision:
    #         self.is_collision = False
    #     self.velocity.y += self.gravity * dt
    #     self.position += self.velocity * dt
    #     self.update_trail()

    # # DRAW

    # def draw_collision_effect(self, surface):
    #     if self.is_collision:
    #         self.collision_effect = self.collision_effect_duration
    #         self.is_collision = False

    #     if self.collision_effect > 0:
    #         progress = self.collision_effect / self.collision_effect_duration

    #         alpha = int(255 * progress)
    #         radius = int(self.radius * (1 + 0.3 * (1 - progress)))

    #         effect = pygame.Surface(
    #             (radius * 2, radius * 2),
    #             pygame.SRCALPHA
    #         )

    #         pygame.gfxdraw.filled_circle(
    #             effect,
    #             radius,
    #             radius,
    #             radius,
    #             (255, 255, 255, alpha)
    #         )

    #         surface.blit(
    #             effect,
    #             (
    #                 int(self.position.x - radius),
    #                 int(self.position.y - radius)
    #             )
    #         )

    #         self.collision_effect -= 1    
    
    # def draw_trail(self, surface):
    #     for i, trail_point in enumerate(self.trail):
    #         red, green, blue = self.color

    #         factor = (i + 1) / len(self.trail)

    #         color = (
    #             int(red * factor),
    #             int(green * factor),
    #             int(blue * factor)
    #         )

    #         radius = max(1, int(self.radius * factor))

    #         pygame.gfxdraw.filled_circle(
    #             surface,
    #             int(trail_point.x),
    #             int(trail_point.y),
    #             radius,
    #             color
    #         )

    # def draw(self, surface):
    #     x = int(self.position.x)
    #     y = int(self.position.y)
    #     r = int(self.radius)

    #     pygame.gfxdraw.aacircle(
    #         surface,
    #         x,
    #         y,
    #         r,
    #         self.color
    #     )

    #     pygame.gfxdraw.filled_circle(
    #         surface,
    #         x,
    #         y,
    #         r,
    #         self.color
    #     )

    #     # Drawing trail
    #     self.draw_trail(surface)

    #     # # Drawing collision effect
    #     # self.draw_collision_effect(surface)

    # # SOUNDS

    # def play_sound(self):
    #     if self.is_collision:
    #         random.choice(self.collision_sounds).play()
