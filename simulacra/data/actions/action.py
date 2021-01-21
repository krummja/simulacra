from __future__ import annotations
from typing import Any, NamedTuple, TYPE_CHECKING

if TYPE_CHECKING:
    from ecstremity import Entity


class Action(NamedTuple):
    entity: Entity
    event: str
    data: Any

    def act(self):
        self.entity.fire_event(self.event, self.data)
