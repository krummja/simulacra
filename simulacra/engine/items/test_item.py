from __future__ import annotations
from typing import TYPE_CHECKING

from engine.actions import common, Action
from engine.items import Item
from engine.actions import ActionWithItem
from engine.components.physics import Physics
from engine.components.inventory import Inventory
from engine.items.door import OpenableState

if TYPE_CHECKING:
    from engine.location import Location


class TestItem(Item, OpenableState):

    def __init__(self: TestItem, location: Location) -> None:
        super().__init__(location)
        self.components['PHYSICS'] = Physics(self, 1)
        self.components['INVENTORY'] = Inventory(self)
        self.interactive = True
        self.suffix = "(closed)"

    def plan_activate(self: TestItem, action: ActionWithItem) -> Action:
        return action

    def action_activate(self: Item, action: ActionWithItem) -> None:
        pass
