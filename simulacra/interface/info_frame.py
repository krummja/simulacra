from __future__ import annotations  # type: ignore
from typing import Dict, TYPE_CHECKING, Tuple

from constants import *
from interface.panel import Panel
from geometry import *

if TYPE_CHECKING:
    import tcod.console as Console


class InfoFrame(Panel):

    def __init__(
            self,
            position: Tuple[str, str]=None,
            parent: Panel=None,
            width: int=0,
            height: int=0,
            margin: int=1,
            vertical_offset: int=0,
            horizontal_offset: int=0,
            fg: Tuple[int, int, int]=(255, 255, 255),
            bg: Tuple[int, int, int]=(0, 0, 0),
            name: str="",
            background: str="",
            path: str="",
            location: str="",
        ) -> None:
        super().__init__(
            position=position,
            parent=parent,
            width=width,
            height=height,
            margin=margin,
            vertical_offset=vertical_offset,
            horizontal_offset=horizontal_offset,
            fg=fg,
            bg=bg
        )

        self.name = name
        self.background = background
        self.path = path
        self.location = location

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].tiles_rgb[self.bounds.indices]["bg"] = self.bg
        consoles['ROOT'].print(
            x=self.x+1, 
            y=self.y+1, 
            string=self.name, 
            fg=self.fg, 
            bg=self.bg
        )

        consoles['ROOT'].print(
            x=self.x+1,
            y=self.y+2,
            string=self.background,
            fg=self.fg,
            bg=self.bg
        )