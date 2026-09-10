import pygame
import config
import random

pygame.init()

# MAP
import entities.wall as wall
import world.map as map

points = [
    (100, 100),
    (100, 400),
    (400, 400),
    (700, 720)
]

wall_1 = wall.Wall(points, config.WALL_THICKNESS, config.WALL_COLOR)
map_1 = map.Map()
map_1.add(wall_1)

# SET WINDOW ICON
icon = pygame.image.load(config.WINDOW_ICON)
pygame.display.set_icon(icon)

# SET DISPLAY
screen = pygame.display.set_mode(
    (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
)
pygame.display.set_caption(config.WINDOW_TITLE)

# SOUNDS
# collision_sounds = [
#     pygame.mixer.Sound(sound) for sound in config.COLLISION_SOUNDS
# ]

# [sound.set_volume(config.SOUNDS_VOLUME) for sound in collision_sounds]

# ENTITIES
from entities.ball import Ball
from managers.entity_manager import EntityManager

entity_manager = EntityManager()

# EFFECTS
from effects.trail_effect import TrailEffect
trail_effect = TrailEffect(config.TRAIL_SIZE)

# ENGINE
from engine import Engine

width, height = pygame.display.get_window_size()
engine = Engine(width, height, map_1, screen, entity_manager)

# MAIN LOOP
running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # CLOSE WINDOW
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ADD TO MANAGER
            x, y = event.pos
            ball = Ball(
                config.BALL_GRAVITY,
                config.BALL_RESTITURATION,
                x,
                y,
                config.BALL_RADIUS,
                random.choice(config.BALL_COLORS)
            )
            ball.add_effect(trail_effect)
            entity_manager.add(ball)

    dt = clock.tick(60) / 1000
    engine.update(dt)
    engine.render()
    pygame.display.flip()

pygame.quit()