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

        if position is None:
            self.x = x
            self.y = y
        else:
            if parent is None:
                if position[0] == "top":
                    self.y = 0 + margin
                elif position[0] == "bottom":
                    self.y = CONSOLE_HEIGHT - self.height - margin
                elif position[0] == "center":
                    self.y = (CONSOLE_HEIGHT - self.height) // 2

                if position[1] == "left":
                    self.x = 0 + margin
                elif position[1] == "right":
                    self.x = CONSOLE_WIDTH - self.width - margin
                elif position[1] == "center":
                    self.x = (CONSOLE_WIDTH - self.width) // 2
            else:
                if position[0] == "top":
                    self.y = self.parent.bounds.top + margin
                elif position[0] == "bottom":
                    self.y = self.parent.bounds.bottom - self.height - margin
                elif position[0] == "center":
                    self.y = (self.parent.bounds.bottom - (
                              self.parent.height // 2)) - (
                              self.height // 2)

                if position[1] == "left":
                    self.x = self.parent.bounds.left + margin
                elif position[1] == "right":
                    self.x = self.parent.bounds.right - self.width - margin
                elif position[1] == "center":
                    self.x = (self.parent.bounds.right - (
                              self.parent.width // 2)) - (
                              self.width // 2)

        self.x += horizontal_offset
        self.y += vertical_offset

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