from __future__ import annotations
from typing import Dict, TYPE_CHECKING
import tcod
from config import *

if TYPE_CHECKING:
    from tcod.console import Console


class Modal:

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.img = tcod.image_new(self.width, self.height)
        
    def on_draw(self, consoles: Dict[str, Console]) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.img.put_pixel(x, y, (50, 50, 50))
        consoles['INTERFACE'].draw_semigraphics(self.img)
        consoles['INTERFACE'].draw_rect(
            self.x, 
            self.y, 
            self.width, 
            self.height,
            ch=0, fg=None, bg=tcod.grey,
            bg_blend=tcod.BKGND_MULTIPLY
            )
        