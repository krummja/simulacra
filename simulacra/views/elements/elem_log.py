from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

from config import *
from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from model import Model
    from model import Message
    from tcod.console import Console


class ElemLog(BaseElement):

    def __init__(self, model: Model) -> None:
        self.log_width = STAGE_PANEL_WIDTH
        super().__init__(ElementConfig(
            position=('bottom', 'left'),
            width=self.log_width, height=(CONSOLE_HEIGHT//4),
            framed=True
        ))
        self.model = model

    def draw_content(self, consoles: Dict[str, Console]) -> None:

        y_index = 0
        x, y = self.bounds.left + 1, self.bounds.bottom - 2
        
        # Print lines above the most recent at a slight dim
        for text in self.model.log[-2::-1]:
            y_index += tcod.console.get_height_rect(self.log_width, str(text))
            if y_index >= 10:
                break
            consoles['ROOT'].print_box(
                x, y - y_index, 
                self.log_width, 0, 
                str(text),
                fg=(100, 100, 100), 
                bg=(0, 0, 0)
                )
            
        # Print the most recent line in full white
        for text in self.model.log[::1]:
            consoles['ROOT'].print_box(
                x, y, 
                self.log_width, 0, 
                str(text) + " " * (self.log_width - len(str(text)) - 2),
                fg=(255, 255, 255), 
                bg=(0, 0, 0)
                )