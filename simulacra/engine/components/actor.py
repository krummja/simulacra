from __future__ import annotations
from typing import Optional, Type, TYPE_CHECKING

import sys
import traceback

from engine.actions import Impossible
from engine.components import Component

if TYPE_CHECKING:
    from engine.actions.behaviors import Behavior
    from engine.event_queue import Event, EventQueue
    from engine.game_object import GameObject
    from engine.location import Location


class Actor(Component):
    """
    The [Actor] is a semantic class that interfaces with the Action system,
    capable of directly enqueueing new Action types.
    """

    def __init__(
            self: Actor,
            game_object: GameObject,
            behavior: Type[Behavior]
        ) -> None:
        super().__init__(game_object)
        self.behavior = behavior(self)
        # self._location = self.game_object.location
        self.game_object.location.area.actors.add(self)
        self.event: Optional[Event] = self.scheduler.schedule(0, self.enqueue)

    @property
    def location(self: Actor) -> Location:
        return self.game_object.location

    @location.setter
    def location(self: Actor, value: Location) -> None:
        self.game_object.location = value

    @property
    def is_player(self: Actor) -> bool:
        result = self.game_object.location.area.player is self.game_object
        return result

    def enqueue(self: Actor, scheduler: EventQueue, event: Event) -> None:
        if event is not self.event:
            return scheduler.unschedule(event)
        try:
            action = self.behavior.plan()
        except Impossible:
            print(f"Unresolved action with {self}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return self.reschedule(100)
        assert action is action.plan(), f"{action} was not fully resolved, {self}."
        action.act()

    @property
    def scheduler(self: Actor) -> EventQueue:
        return self.location.area.model.scheduler

    def reschedule(self: Actor, interval: int) -> None:
        pass

    def __repr__(self: Actor) -> str:
        return f"{self.__class__.__name__}({self.location!r})"
