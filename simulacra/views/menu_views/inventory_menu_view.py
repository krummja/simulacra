from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
from config import *

from view import View
from views.elements.base_element import BaseElement, ElementConfig
from views.base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from entity import Entity
    from tcod.console import Console
    from states.base_menu_state import BaseMenuState


class InventoryMenuView(BaseMenuView):
    
    def __init__(self, state: BaseMenuState) -> None:
        super().__init__(
            state = state,
            config = ElementConfig(
                position = ("bottom", "right"),
                width = SIDE_PANEL_WIDTH,
                height = (SIDE_PANEL_HEIGHT // 2) + 2,
                fg = (255, 255, 255),
                title = "INVENTORY",
                framed=True,
                frame_fg=(255, 0, 255)
                ))
        self._state = state
        
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        self.draw_help(consoles)
        self.draw_inventory(consoles)
        
    def draw_inventory(self, consoles: Dict[str, Console]) -> None:
        data = self._state.data
        
        selected = (255, 0, 255)
        unselected = (255, 255, 255)
        
        i = 0
        for _ in range(len(data)):
            
            char = data[i].char
            name = data[i].name
            fg = data[i].color
            
            consoles['ROOT'].print(
                x = self.x + 2,
                y = self.y + i + 2,
                string = chr(char),
                fg = fg
                )
            
            consoles['ROOT'].print(
                x = self.x + 4,
                y = self.y + i + 2,
                string = name,
                fg = selected if self._state.selection == i else unselected
                )
            
            i += 1