from __future__ import annotations  # type: ignore
from typing import Callable, List, NamedTuple, Optional, TYPE_CHECKING

import heapq


class Event(NamedTuple):
    """An Event represents a specific time and function to call at that time."""
    tick: int
    unique_id: int
    func: Callable[[EventQueue, Event], None]  # type: ignore


class EventQueue:
    
    def __init__(self) -> None:
        self.current_tick = 0
        self.last_unique_id = 0
        self.heap: List[Event] = []

    def schedule(
            self, 
            interval: int, 
            func: Callable[[EventQueue, Event], None]
        ) -> Event:
        """Add a callable object to the event queue.

        `interval` is the time to wait from the current time.

        `func` is the function to call during the scheduled time.
        
        Returns the newly scheduled Event instance.
        """
        event = Event(self.current_tick + interval, self.last_unique_id, func)
        heapq.heappush(self.heap, event)
        self.last_unique_id += 1
        return event

    def reschedule(
            self, 
            event: Event, 
            interval: int, 
            func: Optional[Callable[[EventQueue, Event], None]]=None
        ) -> Event:
        """Reschedule a new Event in place of the existing one.

        `event` must be the currently active Event.

        `interval` is the time to wait from the current time.

        `func` is the function to call during the scheduled time. It may be None
        to reuse the function from `event`.

        Returns the newly scheduled Event instance.
        """
        assert event is not None
        assert self.heap[0] is event
        event = Event(
            self.current_tick + interval, 
            self.last_unique_id, 
            event.func if func is None else func
        )
        heapq.heappushpop(self.heap, event)
        self.last_unique_id += 1
        return event

    def unschedule(self, event: Event) -> None:
        """Explicitly remove the current event.

        `event` must be the currently active Event.
        """
        assert event is not None
        assert self.heap[0] is event
        heapq.heappop(self.heap)

    def invoke_next(self) -> None:
        """Call the next scheduled function.
        
        This expects the scheduled function to take care of removing or
        rescheduling its own Event object. It will fail otherwise.
        """
        event = self.heap[0]
        self.current_tick = event.tick
        event.func(self, event)
        assert event is not self.heap[0], f"{event!r} was not rescheduled."