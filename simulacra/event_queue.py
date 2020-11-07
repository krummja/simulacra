from __future__ import annotations
from typing import Callable, List, NamedTuple, Optional

import heapq


class Event(NamedTuple):
    tick: int
    unique_id: int
    func: Callable[[EventQueue, Event], None]


class EventQueue:

    def __init__(self: EventQueue) -> None:
        self.current_tick: int = 0
        self.last_unique_id: int = 0
        self.queue: List[Event] = []

    def schedule(
            self: EventQueue,
            interval: int,
            func: Callable[[EventQueue, Event], None]
        ) -> Event:
        event = Event(self.current_tick + interval, self.last_unique_id, func)
        heapq.heappush(self.queue, event)
        self.last_unique_id += 1
        return event

    def reschedule(
            self: EventQueue,
            event: Event,
            interval: int,
            func: Optional[Callable[[EventQueue, Event], None]]=None
        ) -> Event:
        assert event is not None
        assert self.queue[0] is event
        event = Event(
            self.current_tick + interval,
            self.last_unique_id,
            event.func if func is None else func
            )
        heapq.heappushpop(self.queue, event)
        self.last_unique_id += 1
        return event

    def unschedule(self: EventQueue, event: Event) -> None:
        assert event is not None
        assert self.queue[0] is event
        heapq.heappop(self.queue)

    def invoke_next(self: EventQueue) -> None:
        event = self.queue[0]
        self.current_tick = event.tick
        event.func(self, event)
        assert event is not self.queue[0], f"{event!r} was not rescheduled."
