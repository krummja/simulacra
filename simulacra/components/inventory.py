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

    def add_to(self, item: Item) -> None:
        if len(self['contents']) < self.slots:
            item.lift()
            item.owner = self
            self['contents'].append(item)
    
    def remove_from(self, item: Item, location: Location) -> None:
        if item in self['contents']:
            item.owner = None
            item.place(location)
            self['contents'].remove(item)