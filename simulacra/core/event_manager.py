from __future__ import annotations
from typing import Callable, NamedTuple, List, Optional, TYPE_CHECKING

import heapq

from .manager import Manager

if TYPE_CHECKING:
    from .game import Game


class Event(NamedTuple):
    tick: int
    uid: int
    func: Callable[[EventManager, Event], None]


class EventManager(Manager):

    def __init__(self, game: Game) -> None:
        self.game = game
        self.current_tick: int = 0
        self.last_uid: int = 0
        self.queue: List[Event] = []

    def schedule(
            self,
            interval: int,
            func: Callable[[EventManager, Event], None]
        ) -> Event:
        event = Event(self.current_tick + interval, self.last_uid, func)
        heapq.heappush(self.queue, event)
        self.last_uid += 1
        return event

    def reschedule(
            self,
            event: Event,
            interval: int,
            func: Optional[Callable[[EventManager, Event], None]] = None
        ) -> Event:
        assert event is not None
        assert self.queue[0] is event
        event = Event(
            self.current_tick + interval,
            self.last_uid,
            event.func if func is None else func
            )
        heapq.heappushpop(self.queue, event)
        self.last_uid += 1
        return event

    def unschedule(self, event: Event) -> None:
        assert event is not None
        assert self.queue[0] is event
        heapq.heappop(self.queue)

    def invoke_next(self) -> None:
        event = self.queue[0]
        self.current_tick = event.tick
        event.func(self, event)
        assert event is not self.queue[0], f"{event!r} was not scheduled."
