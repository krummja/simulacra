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
    _option: str = "consider"

    def __init__(
            self: Actor,
            owner: GameObject,
            behavior: Type[Behavior]
        ) -> None:
        super().__init__(owner)
        self.behavior = behavior(self)
        self.owner.location.area.actors.add(self)
        self.event: Optional[Event] = self.scheduler.schedule(0, self.enqueue)

    @property
    def location(self: Actor) -> Location:
        return self.owner.location

    @property
    def is_player(self: Actor) -> bool:
        result = self.owner.location.area.player is self.owner
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
