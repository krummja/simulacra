from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from collections import defaultdict
from component import Component

if TYPE_CHECKING:
    from item import Item


class EquipmentSlot(defaultdict):
    
    def __init__(self, item: Item = None) -> None:
        self['uid']: str = item.uid
        self['slot']: Optional[Item] = item
        self.equipment_slot = item.slot


class Equipment(Component):
    
    def __init__(self) -> None:
        super().__init__("EQUIPMENT")
        self.equipment_slots = [
            'head', 
            'torso', 
            'shoulders', 
            'back',
            'arms',
            'hands',
            'legs',
            'waist',
            'feet'
            ]
        self.equipped_count = 0

    def equip(self, item: Item) -> None:
        if item.slot in self.equipment_slots and item.equippable:
            item.owner = self
            item.equipped = True
            self.equipped_count += 1
            self.equipment_slots.remove(item.slot)
            self[item.uid] = EquipmentSlot(item)
    
    def remove(self, item: Item) -> None:
        if item.uid in self.keys():
            item: Item = self[item.uid]['slot']
            item.equipped = False
            self.equipped_count -= 1
            self.equipment_slots.append(item.slot)
            del self[item.uid]
