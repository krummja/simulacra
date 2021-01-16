"""ENGINE.EVENTS.Actor

Define an actor for `Entity` types to interface with the `EventQueue`.

Classes:

    Actor
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .action import Impossible

if TYPE_CHECKING:
    from engine.areas.location import Location
    from .control import Control
    from .event_queue import Event, EventQueue
    from .result import Result
    from engine.entities.entity import Entity


class Actor:
    """Base `Actor` object.

    Used as a mixin with an `Entity` to provide a base API for the
    game's `EventQueue`.
    """

    def __init__(self, *, owner: Entity, control: Control) -> None:
        self.owner = owner
        self.control = control
        self.owner.location.area.actor_model.actors.add(self)
        self.event: Optional[Event] = self.scheduler.schedule(0, self.act)

    @property
    def is_player(self) -> bool:
        return self.owner.location.area.player is self.owner

    @property
    def scheduler(self) -> EventQueue:
        return self.owner.location.area.model.scheduler

    def act(self, scheduler: EventQueue, event: Event) -> Optional[Result]:
        """Try to execute a planned `Action`."""
        if event is not self.event:
            return scheduler.unschedule(event)
        try:
            action = self.control.plan()
        except Impossible:
            return self.reschedule(100)
        return action.act()

    def reschedule(self, interval: int) -> None:
        if self.event is None:
            return
        self.event = self.scheduler.reschedule(self.event, interval)
