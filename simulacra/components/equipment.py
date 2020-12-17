from __future__ import annotations
from typing import Dict, TYPE_CHECKING, Hashable

from component import Component

if TYPE_CHECKING:
    from item import Item
    

class EquipmentSlot:
    
    def __init__(self, slot: str) -> None:
        self.slot = slot
        self.item = None
    
    def add_to_slot(self, item: Item) -> None:
        self.item = item
        
    def remove_from_slot(self) -> Item:
        item = self.item
        self.item = None
        return item        
    
    def __hash__(self) -> Hashable:
        return hash(self.item)

    @property
    def description(self) -> str:
        return self.item.description
    
    @property
    def name(self) -> str:
        return self.item.name
    
    @property
    def renderables(self) -> Dict[str, str]:
        return {
            'char': chr(self.item.char),
            'color': self.item.color,
            'name': self.name,
            'description': self.description
            }


class Equipment(Component):
    
    def __init__(self) -> None:
        super().__init__("EQUIPMENT")
        self['left_hand'] = EquipmentSlot('left hand')
        self['right_hand'] = EquipmentSlot('right hand')
        self['head'] = EquipmentSlot('head')
        self['neck'] = EquipmentSlot('neck')
        self['shoulders'] = EquipmentSlot('shoulders')
        self['arms'] = EquipmentSlot('arms')
        self['hands'] = EquipmentSlot('hands')
        self['torso'] = EquipmentSlot('torso')
        self['back'] = EquipmentSlot('back')
        self['waist'] = EquipmentSlot('waist')
        self['legs'] = EquipmentSlot('legs')
        self['feet'] = EquipmentSlot('feet')
        
    def equip(self, slot: str, item: Item) -> None:
        if self[slot].item is None:
            self[slot].add_to_slot(item)
            item.is_equipped = True

    def remove(self, slot: str) -> Item:
        if self[slot].item is not None:
            self[slot].item.is_equipped = False
            return self[slot].remove_from_slot()
            