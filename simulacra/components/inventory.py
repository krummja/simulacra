from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from collections import defaultdict
from component import Component

if TYPE_CHECKING:
    from location import Location
    from item import Item
    

class InventorySlot(defaultdict):
    
    def __init__(self, item: Item = None) -> None:
        self['uid']: str = item.uid
        self['slot']: Optional[Item] = item
        
    def __str__(self) -> str:
        return str(self['uid'])


class Inventory(Component):
   
    def __init__(self) -> None:
        super().__init__("INVENTORY")
        self.slots = 10
        self.is_locked: bool = False

    def take(self, item: Item) -> None:
        assert item.owner is not self
        if self.slots > 0:
            item.lift()
            item.owner = self
            self[item.uid] = InventorySlot(item)
            self.slots -= 1
        else:
            self.owner.location.area.model.report("There's no room...")
    
    def remove(self, item_uid: str):
        assert self[item_uid]
        del self[item_uid]
        