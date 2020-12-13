from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import tcod
from config import *

from view import View
from views.elements.base_element import BaseElement, ElementConfig
from views.elements.help_text_element import HelpTextElement

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

    def draw_help(self, consoles: Dict[str, Console]) -> None:
        help_text = HelpTextElement(
            help_options=[
                "[ENTER]:select, ".upper(),
                "[⬆/⬇]:change selection, ".upper(),
                "[ESC]:back".upper()
            ],
            hue=(255, 0, 0),
            position=("bottom", "left"),
            offset_x=36,
            offset_y=-(CONSOLE_HEIGHT - STAGE_PANEL_HEIGHT)+3)
        help_text.draw(consoles)

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        self.draw_help(consoles)
        
        selected = (255, 0, 255)
        unselected = (255, 255, 255)
        
        data = self._state.data
        y_index = 0
        for i in range(len(data)):
            consoles['ROOT'].print(
                x=self.x + 2, y=self.y + y_index + 2,
                string=data[y_index],
                fg=selected if self._state.selection == y_index else unselected)
            y_index += 1
