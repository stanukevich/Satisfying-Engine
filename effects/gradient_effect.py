from typing import TYPE_CHECKING

from effects.effect import Effect
from entities.modifiers import lerp_color


if TYPE_CHECKING:
    from entities.entity import Entity


class GradientEffect(Effect):
    def __init__(self, smoothness, colors, current_color):
        self.smoothness = smoothness
        self.colors = colors
        self.current_index = colors.index(current_color)
        self.progress = 0

    def update(self, dt, entity: "Entity"):
        current_color = self.colors[self.current_index]
        next_index = (self.current_index + 1) % len(self.colors)
        target_color = self.colors[next_index]

        self.progress += self.smoothness * dt

        if self.progress >= 1:
            self.progress = 0
            self.current_index = next_index
            return

        new_color = lerp_color(
            current_color,
            target_color,
            self.progress
        )

        entity.set_color(new_color)