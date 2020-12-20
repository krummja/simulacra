from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING

import copy

from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from item import Item
    from components.inventory import Inventory
    from tcod.console import Console


class InventoryElement(BaseElement):

    def __init__(self, config: ElementConfig, data: Inventory = None) -> None:
        super().__init__(config)
        if data is not None:
            self._data = [slot for slot in data.get_all_items()]

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        
        y_index = 0
        
        for _ in range(len(self._data)):
            char = self._data[y_index].item.char
            color = self._data[y_index].item.color
            name = self._data[y_index].item.name
            
            if len(name) > 14:
                name = name[0:12] + "."
            
            consoles['ROOT'].tiles_rgb[["ch", "fg"]][
                self.y + y_index + 2, 
                self.x + 2
                ] = char, color
            
            consoles['ROOT'].print(
                x = self.x + 4,
                y = self.y + y_index + 2,
                string = name,
                fg = (255, 255, 255)
                )

            y_index += 1
