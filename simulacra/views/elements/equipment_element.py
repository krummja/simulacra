from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING

from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from item import Item
    from components.equipment import Equipment, EquipmentSlot
    from tcod.console import Console


class EquipmentSlotElement:
    
    def __init__(self, parent: EquipmentElement, data: EquipmentSlot) -> None:
        self.parent = parent
        
        if data.item is not None:
            self.char = data.renderables['char']
            self.color = data.renderables['color']
            self.fg = (255, 255, 255)
            self.name = data.renderables['name']
            self.description = data.renderables['description']
            self.durability = "----------"
        else:
            self.char = "-"
            self.color = (100, 100, 100)
            self.fg = (100, 100, 100)
            self.name = data.slot
            self.description = ""
            self.durability = ""
        
    def draw(self, i: int, consoles: Dict[str, Console]) -> None:
        
        if len(self.name) > 14:
            self.name = self.name[0:12] + "."
        
        consoles['ROOT'].print(
            x = self.parent.x + 2,
            y = self.parent.y + 2 + i,
            string = self.char,
            fg = self.color
            )
        
        consoles['ROOT'].print(
            x = self.parent.x + 4,
            y = self.parent.y + 2 + i,
            string = self.name,
            fg = self.fg
            )
        
        consoles['ROOT'].print(
            x = self.parent.x + 4,
            y = self.parent.y + 3 + i,
            string = self.durability,
            fg = (255, 0, 0)
            )


class EquipmentElement(BaseElement):
    
    def __init__(self, config: ElementConfig, data: Equipment) -> None:
        super().__init__(config)
        self.lhand_slot = EquipmentSlotElement(self, data['left_hand'])
        self.rhand_slot = EquipmentSlotElement(self, data['right_hand'])
        
        self.head_slot = EquipmentSlotElement(self, data['head'])
        self.neck_slot = EquipmentSlotElement(self, data['neck'])
        self.shoulders_slot = EquipmentSlotElement(self, data['shoulders'])
        self.arms_slot = EquipmentSlotElement(self, data['arms'])
        self.hands_slot = EquipmentSlotElement(self, data['hands'])
        self.torso_slot = EquipmentSlotElement(self, data['torso'])
        self.back_slot = EquipmentSlotElement(self, data['back'])
        self.waist_slot = EquipmentSlotElement(self, data['waist'])
        self.legs_slot = EquipmentSlotElement(self, data['legs'])
        self.feet_slot = EquipmentSlotElement(self, data['feet'])
        
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        
        self.lhand_slot.draw(0, consoles)
        self.rhand_slot.draw(2, consoles)
        
        self.head_slot.draw(5, consoles)
        self.neck_slot.draw(7, consoles)
        self.shoulders_slot.draw(9, consoles)
        self.arms_slot.draw(11, consoles)
        self.hands_slot.draw(13, consoles)
        self.torso_slot.draw(15, consoles)
        self.back_slot.draw(17, consoles)
        self.waist_slot.draw(19, consoles)
        self.legs_slot.draw(21, consoles)
        self.feet_slot.draw(23, consoles)