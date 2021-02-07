from __future__ import annotations
from typing import TYPE_CHECKING

from ecstremity import Component

if TYPE_CHECKING:
    from ecstremity import EntityEvent


class Body(Component):

    def on_death(self, event: EntityEvent) -> None:
        if not self.entity.has('Position'):
            return
