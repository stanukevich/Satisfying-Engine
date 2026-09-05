import pygame
import pygame.gfxdraw
import random

class Ball:
    def __init__(self, x, y, radius, ball_colors, collision_sounds, collision_effect_duration, restitution, gravity, trail_size):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.color = random.choice(ball_colors)
        self.velocity = pygame.Vector2(0, 0)
        self.restitution = restitution
        self.gravity = gravity

        self.trail_size = trail_size
        self.trail = []

        self.is_collision = False
        self.collision_sounds = collision_sounds
        self.collision_effect_duration = collision_effect_duration
        self.collision_effect = 0

    # UPDATE

    def update_trail(self):
        self.trail.append(self.position.copy())
        if len(self.trail) > self.trail_size:
            self.trail.pop(0)

    def update(self, dt):
        if self.is_collision:
            self.is_collision = False
        self.velocity.y += self.gravity * dt
        self.position += self.velocity * dt
        self.update_trail()

    # DRAW

    def draw_collision_effect(self, surface):
        if self.is_collision:
            self.collision_effect = self.collision_effect_duration
            self.is_collision = False

        if self.collision_effect > 0:
            progress = self.collision_effect / self.collision_effect_duration

            alpha = int(255 * progress)
            radius = int(self.radius * (1 + 0.3 * (1 - progress)))

            effect = pygame.Surface(
                (radius * 2, radius * 2),
                pygame.SRCALPHA
            )

            pygame.gfxdraw.filled_circle(
                effect,
                radius,
                radius,
                radius,
                (255, 255, 255, alpha)
            )

            surface.blit(
                effect,
                (
                    int(self.position.x - radius),
                    int(self.position.y - radius)
                )
            )

            self.collision_effect -= 1    
    
    def draw_trail(self, surface):
        for i, trail_point in enumerate(self.trail):
            red, green, blue = self.color

            factor = (i + 1) / len(self.trail)

            color = (
                int(red * factor),
                int(green * factor),
                int(blue * factor)
            )

            radius = max(1, int(self.radius * factor))

            pygame.gfxdraw.filled_circle(
                surface,
                int(trail_point.x),
                int(trail_point.y),
                radius,
                color
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

        # Drawing trail
        self.draw_trail(surface)

        # # Drawing collision effect
        # self.draw_collision_effect(surface)

    # SOUNDS

    def play_sound(self):
        if self.is_collision:
            random.choice(self.collision_sounds).play()
