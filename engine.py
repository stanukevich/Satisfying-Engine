from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.ball import Ball
    from world.map import Map
    from managers.entity_manager import EntityManager

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

def check_ball_window_collision(width, height, ball: "Ball"):
    position = ball.position
    radius = ball.radius

    return (
        position.x - radius <= 0
        or position.x + radius >= width
        or position.y - radius <= 0
        or position.y + radius >= height
    )

def resolve_ball_window_collision(width, height, ball: "Ball"):
    position = ball.position
    radius = ball.radius
    velocity = ball.velocity
    restitution = ball.restitution

    if position.x - radius <= 0:
        position.x = radius
        velocity.x *= -1 * restitution

    if position.x + radius >= width:
        position.x = width - radius
        velocity.x *= -1 * restitution

    if position.y - radius <= 0:
        position.y = radius
        velocity.y *= -1 * restitution

    if position.y + radius >= height:
        position.y = height - radius
        velocity.y *= -1 * restitution

def check_ball_ball_collision(ball_a: "Ball", ball_b: "Ball"):
    distance = ball_a.position.distance_to(ball_b.position)
    radius_sum = ball_a.radius + ball_b.radius
    return distance <= radius_sum

def resolve_ball_ball_collision(ball_a: "Ball", ball_b: "Ball"):
    direction = ball_b.position - ball_a.position
    distance = direction.length()

    if distance == 0:
        return

    normal = direction.normalize()

    relative_velocity = ball_b.velocity - ball_a.velocity

    velocity_along_normal = relative_velocity.dot(normal)

    if velocity_along_normal >= 0:
        return

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

class Engine:
    def __init__(self, width, height, map: "Map", surface, entity_manager: "EntityManager"):
        self.window = (width, height)
        self.map = map
        self.surface = surface
        self.entity_manager = entity_manager

    def process_window_collisions(self):
        entities = self.entity_manager.entities
        window = self.window

        for entity in entities:
            entity.process_window_collision(window)

    def process_map_collisions(self):
        entities = self.entity_manager.entities
        map = self.map

        for entity in entities:
            entity.process_map_collision(map)

    def process_entities_collisions(self):
        entities = self.entity_manager.entities

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                entity_a = entities[i]
                entity_b = entities[j]

                entity_a.process_entity_collision(entity_b)

    def process_collisions(self):
        self.process_window_collisions()
        self.process_map_collisions()
        self.process_entities_collisions()

    def update(self, dt):
        entity_manager = self.entity_manager

        entity_manager.update(dt)
        self.process_collisions()

    def draw_entities_effects(self):
        entities = self.entity_manager.entities
        surface = self.surface

        for entity in entities:
            entity.draw_effects(surface)

    def render(self):
        surface = self.surface
        map = self.map
        entity_manager = self.entity_manager

        surface.fill((0, 0, 0))
        map.draw(surface)
        entity_manager.draw(surface)
        self.draw_entities_effects()