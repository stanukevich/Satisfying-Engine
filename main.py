import pygame
import config

pygame.init()

# MAP
import wall
import map

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
collision_sounds = [
    pygame.mixer.Sound(sound) for sound in config.COLLISION_SOUNDS
]

[sound.set_volume(config.SOUNDS_VOLUME) for sound in collision_sounds]

# OBJECTS
from ball import Ball
from ball_manager import BallManager

ball_manager = BallManager()

running = True
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            # CLOSE WINDOW
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # ADD BALL TO MANAGER
            x, y = event.pos
            ball = Ball(
                x,
                y, 
                config.BALL_RADIUS, 
                config.BALL_COLORS,
                collision_sounds, 
                config.COLLISION_EFFECT_DURATION, 
                config.BALL_RESTITURATION, 
                config.BALL_GRAVITY, 
                config.TRAIL_SIZE
            )
            ball_manager.add(ball)

    dt = clock.tick(60) / 1000

    # UPDATE
    width, height = pygame.display.get_window_size()
    ball_manager.update(width, height, map_1, dt)
 
    # RENDERING
    ball_manager.play_sound()
    screen.fill((0, 0, 0))
    map_1.draw(screen)
    ball_manager.draw(screen)
    pygame.display.flip()

pygame.quit()