from ball import Ball
from wall import Wall
from map import Map
import random

# Collisions of balls with screen

def check_screen_collision(ball: Ball, width, height):
    if ball.position.x - ball.radius <= 0:
        ball.position.x = ball.radius
        ball.velocity.x *= -1 * ball.restitution
         # STATUS
        ball.is_collision = True

    if ball.position.x + ball.radius >= width:
        ball.position.x = width - ball.radius
        ball.velocity.x *= -1 * ball.restitution
         # STATUS
        ball.is_collision = True

    if ball.position.y - ball.radius <= 0:
        ball.position.y = ball.radius
        ball.velocity.y *= -1 * ball.restitution
         # STATUS
        ball.is_collision = True

    if ball.position.y + ball.radius >= height:
        ball.position.y = height - ball.radius
        ball.velocity.y *= -1 * ball.restitution
         # STATUS
        ball.is_collision = True

# Collisions of balls with map

def check_circle_segment_collision(ball: Ball, start, end, thickness):
    segment = end - start

    if segment.length_squared() == 0:
        return False

    to_ball = ball.position - start

    t = to_ball.dot(segment) / segment.length_squared()
    t = max(0.0, min(1.0, t))

    closest = start + segment * t

    distance = ball.position.distance_to(closest)

    effective_radius = ball.radius + thickness / 2

    return distance <= effective_radius

def resolve_circle_segment_collision(ball: Ball, start, end, thickness):
    segment = end - start

    if segment.length_squared() == 0:
        return

    to_ball = ball.position - start

    t = to_ball.dot(segment) / segment.length_squared()
    t = max(0.0, min(1.0, t))

    closest = start + segment * t

    delta = ball.position - closest
    distance = delta.length()

    if distance == 0:
        return

    normal = delta.normalize()

    effective_radius = ball.radius + thickness / 2

    penetration = effective_radius - distance

    if penetration > 0:
        ball.position += normal * penetration

    velocity_normal = ball.velocity.dot(normal)

    if velocity_normal < 0:
        ball.velocity -= (
            1 + ball.restitution
        ) * velocity_normal * normal

     # STATUS
    ball.is_collision = True
        
def check_wall_collision(ball: Ball, wall: Wall):
    points = wall.points
    for i in range(len(points) - 1):
        start = points[i]
        end = points[i + 1]
        thickness = wall.thickness
        if(check_circle_segment_collision(ball, start, end, thickness)):
            resolve_circle_segment_collision(ball, start, end, thickness)

def check_map_collision(ball: Ball, map: Map):
    for wall in map.walls:
        check_wall_collision(ball, wall)

# Collisions of balls with each other

def check_collision(ball_a: Ball, ball_b: Ball):
    distance = ball_a.position.distance_to(ball_b.position)
    radius_sum = ball_a.radius + ball_b.radius
    return distance <= radius_sum

def resolve_collision(ball_a: Ball, ball_b: Ball):
    direction = ball_b.position - ball_a.position
    distance = direction.length()

    if distance == 0:
        return

    normal = direction.normalize()

    # RELATIVE VELOCITY
    relative_velocity = ball_b.velocity - ball_a.velocity

    # CLOSING SPEED
    velocity_along_normal = relative_velocity.dot(normal)

    # ARE ALREADY DISPERSING
    if velocity_along_normal >= 0:
        return

    # ELASTIC COLLISION
    impulse = -velocity_along_normal

    ball_a.velocity -= impulse * normal
    ball_b.velocity += impulse * normal

    # RESTITURATION
    ball_a.velocity *= ball_a.restitution
    ball_b.velocity *= ball_b.restitution

    # REMOVING THE INTERSECTION
    radius_sum = ball_a.radius + ball_b.radius
    overlap = radius_sum - distance

    if overlap > 0:
        correction = normal * (overlap / 2)

        ball_a.position -= correction
        ball_b.position += correction

    # STATUS
    ball_a.is_collision = True
    ball_b.is_collision = True

def check_collisions(balls):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball_a = balls[i]
            ball_b = balls[j]

            if check_collision(ball_a, ball_b):
                resolve_collision(ball_a, ball_b)