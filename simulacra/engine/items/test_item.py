from __future__ import annotations
from typing import TYPE_CHECKING

from engine.items import Item
from engine.components.physics import Physics

if TYPE_CHECKING:
    from engine.location import Location


class TestItem(Item):

    def __init__(self: TestItem, location: Location) -> None:
        super().__init__(location)
        self.components['PHYSICS'] = Physics(self, 1)
