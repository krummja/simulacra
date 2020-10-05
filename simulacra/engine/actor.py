from __future__ import annotations
from typing import Optional, Tuple, Type, TYPE_CHECKING

import sys
import traceback

from engine.game_object import GameObject
from engine.actions import Impossible


if TYPE_CHECKING:
    from engine.event_queue import Event, EventQueue
    from engine.location import Location
    from engine.actions.behaviors import Behavior


class Actor:

    def __init__(
            self: Actor,
            location: Location,
            game_object: GameObject,
            behavior: Type[Behavior]
        ) -> None:
        self.location = location
        location.area.actors.add(self)
        self.game_object = game_object
        self.behavior = behavior(self)
        self.event: Optional[Event] = self.scheduler.schedule(0, self.enqueue)

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

    def is_player(self: Actor) -> bool:
        return self.location.area.player is self

    def __repr__(self: Actor) -> str:
        return f"{self.__class__.__name__}({self.location!r})"
