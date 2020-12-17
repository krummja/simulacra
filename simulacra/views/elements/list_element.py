from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING, Tuple, Optional

from contextlib import suppress
import tcod
from config import *
from message import ColorFormatter, ConsoleText

from view import View
from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from component import Component
    from tcod.console import Console
    from state import State
    from entity import Entity
    

class ListElement(BaseElement):
    """A static list GUI element. 
    
    To get a selectable list element, extend the BaseMenuState and BaseMenuView 
    classes instead.
    """
    
    def __init__(self, config: ElementConfig, data: Component = None) -> None:
        super().__init__(config)
        self._data = []
        if data is not None:
            self._entries = [(k, v) for k, v in data.items()]
            self._data = [entry[1]['slot'] for entry in self._entries]
        
    @property
    def data(self) -> ListData:
        return self._data
    
    def update(self, data: List[Entity]) -> None:
        self._data = data
    
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        y_index = 0
                
        for _ in range(len(self._data)):
            
            # Draw the entity's icon
            consoles['ROOT'].print(
                x=self.x + 2, 
                y=self.y + y_index + 2,
                string=chr(self._data[y_index].char),
                fg=self._data[y_index].color
                )
            
            # Draw the entity name
            consoles['ROOT'].print(
                x=self.x + 4, 
                y=self.y + y_index + 2,
                string=self._data[y_index].noun_text,
                fg=(255, 255, 255)
                )
            
            y_index += 1