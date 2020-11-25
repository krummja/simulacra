from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
from config import *

if TYPE_CHECKING:
    from tcod.console import Console


class InterfaceElement:
    
    def __init__(
            self,
            uid: str,
            x: int = 0,
            y: int = 0,
            width: int = CONSOLE_WIDTH,
            height: int = CONSOLE_HEIGHT,
            title: str = "",
            string: str = "",
        ) -> None:
        self.uid = uid
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.string = string
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        consoles['INTERFACE'].draw_rect(
            self.x, self.y, 
            self.width, self.height,
            ch=0, fg=tcod.white, bg=tcod.gray,
            bg_blend=tcod.BKGND_MULTIPLY
            )
        
        consoles['INTERFACE'].draw_frame(
            self.x, self.y,
            self.width, self.height,
            title="test frame",
            )
       
        consoles['INTERFACE'].blit(
            consoles['ROOT'], 
            self.x, self.y, self.x, self.y,
            self.width, self.height,
            fg_alpha=1.0, bg_alpha=0.3
        )
        
        # consoles['ROOT'].print_box(
        #     self.x+2, self.y+2,
        #     self.width-4, self.height-4,
        #     string=self.string
        #     )
        