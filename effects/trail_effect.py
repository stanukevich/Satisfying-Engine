from effects.effect import Effect

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.entity import Entity

class TrailEffect(Effect):
    def __init__(self, size):
        self.size = size
        self.points = []

    def add_points(self, entity: "Entity"):
        position = entity.get_position()
        self.points.append(position.copy())

    def pop_points(self):
        self.points.pop(0)

    def draw(self, surface, entity: "Entity"):
        super().draw(surface, entity)

        self.add_points(entity)
        if len(self.points) > self.size:
            self.pop_points()

        for i, point in enumerate(self.points):
            factor = (i + 1) / len(self.points)
            entity.draw_transformed(surface, factor, point)