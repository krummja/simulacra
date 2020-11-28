from __future__ import annotations
from typing import List, TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from item import Item
    

class Inventory(Component):
   
    ident = "INVENTORY"
    
    def __init__(self) -> None:
        super().__init__()
        self._contents: List[Item] = []

    @property
    def contents(self) -> List[Item]:
        return self._contents

    def take(self, item: Item) -> None:
        item.lift()
        self._contents.append(item)
        item.owner = self
    
    def __repr__(self):
        if len(self._contents) > 0:
            return [item.noun_text for item in self._contents]
        else:
            return "Empty"