from typing import TYPE_CHECKING

from entities.collisions import (
    process_window_collisions,
    process_map_collisions,
    process_entities_collisions
)


if TYPE_CHECKING:
    from world.map import Map
    from managers.entity_manager import EntityManager
    from managers.effect_manager import EffectManager
    

class Engine:
    def __init__(self, width, height, map: "Map", surface, entity_manager: "EntityManager", effect_manager: "EffectManager"):
        self.window = (width, height)
        self.map = map
        self.surface = surface

        self.entity_manager = entity_manager
        self.effect_manager = effect_manager

    def update(self, dt):
        self.entity_manager.update(dt)
        self.effect_manager.update(dt)

        entities = self.entity_manager.entities

        process_window_collisions(self.window, entities)
        process_map_collisions(self.map, entities)
        process_entities_collisions(entities)

    def render(self):
        surface = self.surface

        surface.fill((0, 0, 0))

        self.map.draw(surface)
        self.entity_manager.draw(surface)
        self.effect_manager.draw(surface)