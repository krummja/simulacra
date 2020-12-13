from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING, Tuple

import tcod
from config import *
from message import ColorFormatter, ConsoleText

from view import View
from views.elements.base_element import BaseElement, ElementConfig


if TYPE_CHECKING:
    from tcod.console import Console
    from state import State
    

class HelpTextElement(BaseElement):
    
    def __init__(
            self, 
            help_options: List[str], 
            hue: Tuple[int, int, int],
            position=("bottom", "center"),
            offset_x=0,
            offset_y=0,
        ) -> None:
        super().__init__(ElementConfig(
            position=position,
            width=CONSOLE_WIDTH,
            height=3,
            offset_x=offset_x,
            offset_y=offset_y
            ))
        
        self.help_options = []
        for item in help_options:
            item = item.split(":")
            cmd = ColorFormatter(hue).format(item[0])
            self.help_options.append(cmd + " " + item[1])
        
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        help_text = ""
        for item in self.help_options:
            help_text = help_text + item
        text_width = len(help_text)
        
        consoles['ROOT'].print(
            ((self.content.width - text_width - self.offset_x) // 2),
            self.content.top,
            help_text,
            fg=self.fg,
            bg=self.bg
            )