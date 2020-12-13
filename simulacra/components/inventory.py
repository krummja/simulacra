from __future__ import annotations
from typing import List, TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from location import Location
    from item import Item
    

class Inventory(Component):
   
    def __init__(self, slots: int = 10) -> None:
        super().__init__("INVENTORY")
        self['contents']: List[Item] = []
        self.slots = slots        
        self.is_locked: bool = False

    def take(self, item: Item) -> None:
        assert item.owner is not self
        item.lift()
        self['contents'].append(item)
        item.owner = self