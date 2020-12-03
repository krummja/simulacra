from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING, Tuple, Optional

import tcod
from config import *
from message import ColorFormatter, ConsoleText

from view import View
from views.elements.base_element import BaseElement, ElementConfig
from states.base_menu_state import ListData


if TYPE_CHECKING:
    from tcod.console import Console
    from state import State
    from entity import Entity
    

class ListElement(BaseElement):
    """A static list GUI element. 
    
    To get a selectable list element, extend the BaseMenuState and BaseMenuView 
    classes instead.
    """
    
    def __init__(self, config: ElementConfig, data: List[Entity]) -> None:
        super().__init__(config)
        self._data = data
        
    @property
    def data(self) -> ListData:
        return ListData(self._data)
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        y_index = 0
        for i in range(len(self.data)):
            consoles['ROOT'].print(
                x=self.x+2, y=self.y+y_index+2,
                string=self.data[y_index],
                fg=self.fg)
            y_index += 1