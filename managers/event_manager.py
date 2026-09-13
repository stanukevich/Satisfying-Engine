from typing import TYPE_CHECKING

from managers.manager import Manager


if TYPE_CHECKING:
    from events.event import Event


class EventManager(Manager):
    def __init__(self):
        self.events = []

    def add(self, event: "Event"):
        self.events.append(event)

    def get_events(self):
        return self.events

    def clear(self):
        self.events.clear()