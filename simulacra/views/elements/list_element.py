from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING, Tuple, Optional

import tcod
from config import *
from message import ColorFormatter, ConsoleText

from view import View
from views.elements.base_element import BaseElement, ElementConfig


if TYPE_CHECKING:
    from tcod.console import Console
    from state import State
    from entity import Entity
    

class ListElement(BaseElement):
    """A static list GUI element. 
    
    To get a selectable list element, extend the BaseMenuState and BaseMenuView 
    classes instead.
    """
    
    def __init__(self, config: ElementConfig, data: List[Entity]=[]) -> None:
        super().__init__(config)
        self._data = [entity for entity in data]
        
    @property
    def data(self) -> ListData:
        return self._data
    
    def update(self, data: List[Entity]) -> None:
        self._data = [entity for entity in data]
        
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        y_index = 0
        
        
        for _ in range(len(self._data)):
            char = self._data[y_index].char
            color = self._data[y_index].color
            
            consoles['ROOT'].print(
                x=self.x+2, y=self.y+y_index+2,
                string=chr(char),
                fg=color)
            
            consoles['ROOT'].print(
                x=self.x+4, y=self.y+y_index+2,
                string=self._data[y_index].noun_text,
                fg=self.fg)
            y_index += 1