from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from collections import defaultdict
from component import Component

if TYPE_CHECKING:
    from item import Item


class NonceItem:
    def __init__(self, slot: str) -> None:
        self.uid = ""
        self.char = ord('-')
        self.color = (100, 100, 100)
        self.alt_fg = (100, 100, 100)
        self.noun_text = slot


class EquipmentSlot(defaultdict):
    
    def __init__(self, bodypart: str = None, item: Item = None) -> None:
        if item is None:
            item = NonceItem(bodypart)
        self['uid']: str = item.uid
        self['bodypart']: str = bodypart
        self['slot']: Optional[Item] = item 


class Equipment(Component):
    
    def __init__(self) -> None:
        super().__init__("EQUIPMENT")
        self['head'] = EquipmentSlot('head', None)
        self['neck'] = EquipmentSlot('neck', None)
        self['shoulders'] = EquipmentSlot('shoulders', None)
        self['torso'] = EquipmentSlot('torso', None)
        self['back'] = EquipmentSlot('back', None)
        self['arms'] = EquipmentSlot('arms', None)
        self['legs'] = EquipmentSlot('legs', None)
        self['hands'] = EquipmentSlot('hands', None)
        self['feet'] = EquipmentSlot('feet', None)
            
    def equip(self, slot: str, item: Item) -> None:
        if self[slot]['slot'] is not None:
            self[slot] = EquipmentSlot(slot, item)
        else:
            self.owner.location.area.model.report("Already something there!")
    
    def unequip(self, slot: str) -> None:
        if self[slot]['slot'] is not None:
            del self[slot]
            self[slot] = EquipmentSlot(slot, None)
        else:
            self.owner.location.area.model.report("Nothing to unequip!")