from __future__ import annotations
from typing import Callable, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ecstremity import Entity


class Impossible(Exception):
    """Halt the current action attempt and send a message to the log."""


@dataclass
class Action:
    entity: Entity
    event: str
    data: Any
    condition: Callable[[], bool] = None
    cost: int = 0

    @property
    def success(self) -> bool:
        return self._success

    @success.setter
    def success(self, value: bool) -> None:
        self._success = value

    def plan(self) -> Optional[Action]:
        if self.condition:
            self.success = self.condition()
        return self

    def act(self) -> None:
        """Act step, which fires the event for an action success."""
        self.entity['Actor'].reduce_energy(self.cost)
        self.entity.fire_event(self.event, (self.success, self.data))
