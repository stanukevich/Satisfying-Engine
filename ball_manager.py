import physics
from map import Map

class BallManager:
    def __init__(self):
        self.balls = []

    def add(self, ball):
        self.balls.append(ball)

    def update(self, width, height, map: Map, dt):
        for ball in self.balls:
            ball.update(dt)  

             # Collisions of balls with screen
            physics.check_screen_collision(ball, width, height)  

            # Collisions of balls with map
            physics.check_map_collision(ball, map)

        # Collisions of balls with each other
        physics.check_collisions(self.balls)  

    def draw(self, surface):
        # DRAWING ALL BALLS
        for ball in self.balls:
            ball.draw(surface)

    def play_sound(self):
        for ball in self.balls:
            ball.play_sound()