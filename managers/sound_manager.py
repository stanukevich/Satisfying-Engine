from typing import TYPE_CHECKING

from config import (
    COLLISION_SOUND
)
from managers.manager import Manager
from entities.collisions import CollisionType
from audio.sound import Sound


if TYPE_CHECKING:
    from events.event import Event


class SoundManager(Manager):
    def __init__(self):
        self.sounds = []

    def process(self, events: list["Event"]):
        for event in events:
            if event.type in (
                CollisionType.ENTITY_ENTITY,
                CollisionType.ENTITY_WINDOW,
                CollisionType.ENTITY_WALL,
            ):
                impact = event.get_impact()
                volume = round(impact, 2)
                sound = Sound(COLLISION_SOUND, volume)
                self.sounds.append(sound)

    def play(self):
        for sound in self.sounds:
            sound.play()
            
        self.sounds.clear()