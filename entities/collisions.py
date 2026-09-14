from typing import TYPE_CHECKING
from enum import Enum

from pygame import Vector2

from config import STOP_THRESHOLD

if TYPE_CHECKING:
    from entities.ball import Ball
    from world.map import Map
    from entities.entity import Entity
    from events.event import Event


class CollisionType(Enum):
    ENTITY_WALL = "entity_wall"
    ENTITY_WINDOW = "entity_window"
    ENTITY_ENTITY = "entity_entity"


# COLLISIONS BETWEEN MAP & ENTITIES

def check_ball_segment_collision(start, end, thickness, ball: "Ball"):

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

def resolve_ball_segment_collision(start, end, thickness, ball: "Ball"):

    segment = end - start

    if segment.length_squared() == 0:
        return 0

    to_ball = ball.position - start

    t = to_ball.dot(segment) / segment.length_squared()
    t = max(0.0, min(1.0, t))

    closest = start + segment * t

    delta = ball.position - closest
    distance = delta.length()

    if distance == 0:
        return 0

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

    impact = abs(velocity_normal)

    return impact

def process_map_collisions(map: "Map", entities: list["Entity"], events: list["Event"]):
    for entity in entities:
        entity.process_map_collision(map, events)

# COLLISIONS BETWEEN WINDOW & ENTITIES

def check_ball_window_collision(width, height, ball: "Ball"):
    position = ball.position
    radius = ball.radius
    velocity = ball.velocity

    return (
        (position.x - radius <= 0 and velocity.x < 0)
        or
        (position.x + radius >= width and velocity.x > 0)
        or
        (position.y - radius <= 0 and velocity.y < 0)
        or
        (position.y + radius >= height and velocity.y > 0)
    )

def resolve_ball_window_collision(width, height, ball: "Ball"):
    position = ball.position
    radius = ball.radius
    velocity = ball.velocity
    restitution = ball.restitution

    normal = Vector2(0, 0)

    if position.x - radius <= 0:
        position.x = radius
        normal += Vector2(1, 0)

    if position.x + radius >= width:
        position.x = width - radius
        normal += Vector2(-1, 0)

    if position.y - radius <= 0:
        position.y = radius
        normal += Vector2(0, 1)

    if position.y + radius >= height:
        position.y = height - radius
        normal += Vector2(0, -1)

    if normal.length_squared() == 0:
        return 0

    normal.normalize_ip()

    velocity_normal = velocity.dot(normal)

    if velocity_normal >= 0:
        return 0

    impact = abs(velocity_normal)

    if impact < STOP_THRESHOLD:
        velocity -= velocity_normal * normal
        # if position.y + radius >= height:
        #     position.y = height - radius
        #     velocity.y = 0
        return impact

    velocity -= (
        1 + restitution
    ) * velocity_normal * normal

    return impact

def process_window_collisions(window, entities: list["Entity"], events: list["Event"]):
    for entity in entities:
        entity.process_window_collision(window, events)

# COLLISIONS BETWEEN ENTITIES & ENTITIES

def check_ball_ball_collision(ball_a: "Ball", ball_b: "Ball"):
    distance = ball_a.position.distance_to(ball_b.position)
    radius_sum = ball_a.radius + ball_b.radius
    return distance <= radius_sum

def resolve_ball_ball_collision(ball_a: "Ball", ball_b: "Ball"):
    direction = ball_b.position - ball_a.position
    distance = direction.length()

    if distance == 0:
        return 0

    normal = direction.normalize()

    relative_velocity = ball_b.velocity - ball_a.velocity

    velocity_along_normal = relative_velocity.dot(normal)

    if velocity_along_normal >= 0:
        return 0

    impulse = -velocity_along_normal

    ball_a.velocity -= impulse * normal
    ball_b.velocity += impulse * normal

    ball_a.velocity *= ball_a.restitution
    ball_b.velocity *= ball_b.restitution

    radius_sum = ball_a.radius + ball_b.radius
    overlap = radius_sum - distance

    if overlap > 0:
        correction = normal * (overlap / 2)

        ball_a.position -= correction
        ball_b.position += correction

    impact = abs(velocity_along_normal)

    return impact

def process_entities_collisions(entities: list["Entity"], events: list["Event"]):
    for i in range(len(entities)):
        for j in range(i + 1, len(entities)):
            entity_a = entities[i]
            entity_b = entities[j]

            entity_a.process_entity_collision(entity_b, events)
