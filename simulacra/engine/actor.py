from __future__ import annotations  # type: ignore
from typing import Optional, Type, TYPE_CHECKING

import sys
import traceback

if TYPE_CHECKING:
    from engine.backgrounds import Background
    from engine.paths import Path
    from .location import Location
    from .queue import Event, EventQueue
    from .actions import (Impossible, Action)


# TODO: I need to reorganize this so that there is a 'data' object that holds
# TODO: all of the character's data like name, level, etc.
class Actor:
    
    def __init__(self, location: Location, character, ai_cls: Type[Action]) -> None:
        self.location = location
        self.character = character
        location.area.actors.add(self)

        self.event: Optional[Event] = self.scheduler.schedule(0, self.act)
        self.ai = ai_cls(self)

    def act(self, scheduler: EventQueue, event: Event) -> None:
        if event is not self.event:
            return scheduler.unschedule(event)
        try:
            action = self.ai.plan()
        except Impossible:
            print(f"Unresolved action with {self}!", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            return self.reschedule(100)
        assert action is action.plan(), f"{action} was not fully resolved, {self}."
        action.act()

    @property
    def background(self) -> Background:
        return self.character.background

    @property
    def path(self) -> Path:
        return self.character.path

    @property
    def scheduler(self) -> EventQueue:
        return self.location.area.model.scheduler

    def reschedule(self, interval: int) -> None:
        if self.event is None:
            return
        self.event = self.scheduler.reschedule(self.event, interval)

    def is_visible(self) -> bool:
        return bool(self.location.area.visible[self.location.ij])

    def is_player(self) -> bool:
        return self.location.area.player is self