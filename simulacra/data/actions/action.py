from __future__ import annotations
from typing import Any, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


class Action(NamedTuple):
    entity: Entity
    event: str
    data: Any

    def act(self):
        """Act step, which fires the event for an action success."""
        self.entity.fire_event(self.event, self.data)
