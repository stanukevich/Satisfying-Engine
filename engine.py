from typing import TYPE_CHECKING

from managers.entity_manager import EntityManager
from managers.event_manager import EventManager
from managers.effect_manager import EffectManager
from managers.sound_manager import SoundManager
from entities.collisions import (
    process_window_collisions,
    process_map_collisions,
    process_entities_collisions
)


if TYPE_CHECKING:
    from world.map import Map
    

class Engine:
    def __init__(self, width, height, map: "Map", surface):
        self.window = (width, height)
        self.map = map
        self.surface = surface

        self.entity_manager = EntityManager()
        self.event_manager = EventManager()
        self.effect_manager = EffectManager()
        self.sound_manager = SoundManager()

    def update(self, dt):
        self.entity_manager.update(dt)
        self.effect_manager.update(dt)

        entities = self.entity_manager.get_entities()
        events = self.event_manager.get_events()

        process_window_collisions(self.window, entities, events)
        process_map_collisions(self.map, entities, events)
        process_entities_collisions(entities, events)

        self.sound_manager.process(events)

        self.event_manager.clear()

    def render(self):
        surface = self.surface

        surface.fill((0, 0, 0))

        self.map.draw(surface)
        self.entity_manager.draw(surface)
        self.effect_manager.draw(surface)

        self.sound_manager.play()