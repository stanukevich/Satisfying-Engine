import random

import pygame

import config
from engine import Engine
from managers.entity_manager import EntityManager
from managers.effect_manager import EffectManager
from world.map import Map
from entities.ball import Ball
from entities.wall import Wall
from effects.trail_effect import TrailEffect
from effects.gradient_effect import GradientEffect

# CREATE MAP
points = [
    (100, 100),
    (100, 400),
    (400, 400),
    (700, 720)
]

wall_1 = Wall(points, config.WALL_THICKNESS, config.WALL_COLOR)
map_1 = Map()
map_1.add(wall_1)

# MANAGERS
entity_manager = EntityManager()
effect_manager = EffectManager()

# INITIALIZATION
pygame.init()

# SET WINDOW ICON
icon = pygame.image.load(config.WINDOW_ICON)
pygame.display.set_icon(icon)

# SET DISPLAY
screen = pygame.display.set_mode(
    (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
)
pygame.display.set_caption(config.WINDOW_TITLE)

# ENGINE
width, height = pygame.display.get_window_size()
engine = Engine(width, height, map_1, screen, entity_manager, effect_manager)

# MAIN LOOP
running = True
clock = pygame.time.Clock() 

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # CLOSE WINDOW
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Create trail effect
            trail_effect = TrailEffect(config.TRAIL_SIZE)
            # Create gradient effect
            gradient_effect = GradientEffect(config.GRADIENT_SMOOTHNESS, config.BALL_COLORS)

            # Create ball
            x, y = event.pos
            ball = Ball(
                config.BALL_GRAVITY,
                config.BALL_RESTITURATION,
                x,
                y,
                config.BALL_RADIUS,
                random.choice(config.BALL_COLORS)
            )

            # Add to managers
            entity_manager.add(ball)
            effect_manager.add(ball, trail_effect)
            effect_manager.add(ball, gradient_effect)

    dt = clock.tick(60) / 1000
    engine.update(dt)
    engine.render()
    pygame.display.flip()

pygame.quit()