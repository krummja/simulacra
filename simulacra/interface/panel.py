from __future__ import annotations  # type: ignore
from typing import Dict, Optional, TYPE_CHECKING, Tuple

from geometry import *
from constants import *

if TYPE_CHECKING:
    import tcod.console as Console


class Panel:

    def __init__(
            self,
            x: int=0,
            y: int=0,
            position: Tuple[str, str]=None,
            parent: Panel=None,
            width: int=0,
            height: int=0,
            margin: int=0,
            vertical_offset: int=0,
            horizontal_offset: int=0,
            fg: Tuple[int, int, int]=(255, 255, 255),
            bg: Tuple[int, int, int]=(0, 0, 0),
        ) -> None:
        self.width = width
        self.height = height
        self.parent = parent

        if parent is None:
            parent_top = 0
            parent_bottom = CONSOLE_HEIGHT
            parent_left = 0
            parent_right = CONSOLE_WIDTH
        else:
            parent_top = self.parent.bounds.top
            parent_bottom = self.parent.bounds.bottom
            parent_left = self.parent.bounds.left
            parent_right = self.parent.bounds.right

        if position is None:
            self.x = x
            self.y = y
        else:
            if position[0] == "top":
                self.y = parent_top + margin
            elif position[0] == "bottom":
                self.y = parent_bottom - self.height - margin
            elif position[0] == "center":
                self.y = (parent_bottom - self.height) // 2
            
            if position[1] == "left":
                self.x = parent_left + margin
            elif position[1] == "right":
                self.x = parent_right - self.width - margin
            elif position[1] == "center":
                self.x = (parent_right - self.width) // 2
                # self.x = parent_right - self.width - (self.width // 2)

        self.x = self.x + horizontal_offset
        self.y = self.y + vertical_offset

        self.bounds = Rect.from_edges(
            top=self.y, 
            bottom=self.y+self.height, 
            left=self.x, 
            right=self.x+self.width
        )

        self.fg = fg
        self.bg = bg

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].tiles_rgb[self.bounds.indices]["ch"] = 127
        consoles['ROOT'].tiles_rgb[self.bounds.indices]["fg"] = self.bg
        consoles['ROOT'].tiles_rgb[self.bounds.indices]["bg"] = self.bg