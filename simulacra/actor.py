from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import sys
import traceback

from action import Impossible

if TYPE_CHECKING:
    from control import Control
    from entity import Entity
    from event_queue import Event, EventQueue
    from location import Location


class Actor:

    def __init__(self, owner: Entity, control: Control) -> None:
        self.owner = owner
        self.control = control
        self.owner.location.area.actor_model.actors.add(self)
        self.event: Optional[Event] = self.scheduler.schedule(0, self.act)

    @property
    def location(self) -> Location:
        return self.owner.location

    @location.setter
    def location(self, value: Location) -> None:
        self.owner.location = value

    @property
    def is_player(self) -> bool:
        return self.owner.location.area.player is self.owner

    @property
    def scheduler(self) -> EventQueue:
        return self.owner.location.area.model.scheduler

    def act(self, scheduler: EventQueue, event: Event) -> None:
        if event is not self.event:
            return scheduler.unschedule(event)
        try:
            action = self.control.plan()
        except Impossible:
            print(f"Unresolved action with {self}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return self.reschedule(100)
        assert action is action.plan(), f"{action} not fully resolved, {self}."
        action.act()

    def reschedule(self, interval: int) -> None:
        if self.event is None:
            return
        self.event = self.scheduler.reschedule(self.event, interval)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.owner.location!r})"
