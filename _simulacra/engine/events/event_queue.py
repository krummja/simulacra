"""ENGINE.EVENTS.Event_Queue"""
from __future__ import annotations

import heapq
from typing import TYPE_CHECKING, Callable, List, NamedTuple, Optional

if TYPE_CHECKING:
    from result import Result


class Event(NamedTuple):
    """Representation of a discrete Actor Event.

    `tick` is the current time segment.
    `unique_id` is the uniquely identifiable index of the event.
    `func` is an `Actor.act` method, usually from some controller class.
    """
    tick: int
    unique_id: int
    func: Callable[[EventQueue, Event], None]


class EventQueue:
    """The central queue that handles `Actor` scheduling."""

    def __init__(self) -> None:
        self.current_tick: int = 0
        self.last_unique_id: int = 0
        self.queue: List[Event] = []

    def schedule(
            self,
            interval: int,
            func: Callable[[EventQueue, Event], None]
        ) -> Event:
        """Enqueue an Actor to execute their action turn."""
        event = Event(self.current_tick + interval, self.last_unique_id, func)
        heapq.heappush(self.queue, event)
        self.last_unique_id += 1
        return event

    def reschedule(
            self,
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

    def unschedule(self, event: Event) -> None:
        assert event is not None
        assert self.queue[0] is event
        heapq.heappop(self.queue)

    def invoke_next(self) -> None:
        """Advance the Actor queue and execute the `act` method of the
        next Actor in queue.
        """
        event = self.queue[0]
        self.current_tick = event.tick
        event.func(self, event)
        assert event is not self.queue[0], f"{event!r} was not rescheduled."
