from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import tcod
from config import *

from view import View
from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from entity import Entity
    from tcod.console import Console
    from state import State


class BaseMenuView(View, BaseElement):
    """The base view object for indexed menus that can be navigated through.
    
    Do not make instances of this class directly; instead, make a subclass
    that configures itself with an ElementConfig. Then, pass that sublclass
    into a BaseMenuState subclass during its construction.
    """
    
    def __init__(self, state: State, config: ElementConfig) -> None:
        View.__init__(self, state)
        BaseElement.__init__(self, config)

    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        data = self._state.data
        y_index = 0
        selected = (255, 0, 255)
        unselected = (255, 255, 255)
        for i in range(len(data)):
            consoles['ROOT'].print(
                x=2, y=y_index+2,
                string=data[y_index],
                fg=selected if self._state.selection == y_index else unselected)
            y_index += 1