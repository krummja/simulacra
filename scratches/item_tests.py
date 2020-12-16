from __future__ import annotations
from typing import Hashable


class Item:
    
    def __init__(self, uid, name="", description="") -> None:
        self.uid = uid
        self._name = name
        self._description = description
        
    @property
    def name(self) -> str:
        return self._name
        
    @property
    def description(self) -> str:
        return self._description
    
    def __eq__(self, other: Item) -> bool:
        return (self.uid == other.uid,
                self.name == other.name,
                self.description == other.description)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.uid,
                     self.name,
                     self.description))
        

first_item = Item("item_1", name="Test Item", description="An item...")
second_item = Item("item_2", name="Test Item", description="An item...")

print(first_item == second_item)

test_inventory = {
    'slots': {}
}

test_inventory['slots'][first_item] = "foo"

print(isinstance(first_item, Hashable))
