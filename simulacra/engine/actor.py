from __future__ import annotations  # type: ignore
from typing import Optional, Type, TYPE_CHECKING, Union

import sys
import traceback

from engine.actions import Impossible
from engine.items.other import Corpse

if TYPE_CHECKING:
    from engine.backgrounds import Background
    from engine.paths import Path
    from .location import Location
    from .queue import Event, EventQueue
    from .actions import (Impossible, Action)
    from engine.objects import Object
    from engine.character import Character

GameObject = Union[Character, Object]


class Actor:
    
    def __init__(self, location: Location, obj: GameObject, ai_cls: Type[Action]) -> None:
        self.location = location
        if isinstance(obj, Character):
            self.character = obj
        elif isinstance(obj, Object):
            self.object = obj
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

    # TODO: part of Physics component
    def is_visible(self) -> bool:
        return bool(self.location.area.visible[self.location.ij])

    # TODO: part of Killable component
    def is_combatant(self) -> bool:
        return self.character.combat_flag

    def is_player(self) -> bool:
        return self.location.area.player is self

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.location!r}, {self.character!r})"

    # TODO: Killable component
    def die(self) -> None:
        assert self.character.alive
        self.character.alive = False
        if self.is_visible():
            if self.is_player():
                self.location.area.model.report("You have died...")
            else:
                self.location.area.model.report(f"The {self.character.name} dies.")
        Corpse(self).place(self.location)
        self.location.area.actors.remove(self)
        if self.scheduler.heap[0] is self.event:
            # If the actor died durring its turn, modify the event queue.
            self.scheduler.unschedule(self.event)
        self.event = None  # Disable AI

    # TODO: Part of Killable component
    def damage(self, damage: int) -> None:
        assert damage >= 0
        self.character.attributes['health'].current_value -= damage
        if self.character.attributes['health'].current_value <= 0:
            self.die()
