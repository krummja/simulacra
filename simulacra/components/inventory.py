from __future__ import annotations
from typing import List, TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from item import Item
    

class Inventory(Component):
    """A list of items that can be displayed and selected from.
    
    Attributes:
        _contents       A list of items contained in this Inventory.
        contents        Getter attribute for `_contents`.
        take            Method responsible for mutating `_contents`.
    """
   
    def __init__(self, slots: int = 10) -> None:
        super().__init__("INVENTORY")
        self._slots = slots
        self._contents: List[Item] = []
        
        self.is_locked = False

    def contents(self) -> List[Item]:
        return self._contents

    def take(self, item: Item) -> None:
        # TODO: Offload this to a manager class
        assert item.owner is not self
        item.lift()
        self._contents.append(item)
        item.owner = self