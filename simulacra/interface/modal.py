from __future__ import annotations  # type: ignore
from typing import Dict, TYPE_CHECKING, Tuple

from constants import *
from interface.panel import Panel
from geometry import *

if TYPE_CHECKING:
    import tcod.console as Console


class Modal(Panel):

    def __init__(
            self,
            width: int,
            height: int,
            fg: Tuple[int, int, int],
            bg: Tuple[int, int, int]
        ) -> None:
        super().__init__(
            width=width, 
            height=height,
            position=("center", "center"),
            fg=fg,
            bg=bg
        )
        self._title: str = ""

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def on_draw(self, consoles: Dict[Console]) -> None:
        consoles['ROOT'].draw_frame(
            x=self.x, 
            y=self.y,
            width=self.width, 
            height=self.height,
            title=self.title,
            fg=self.fg, 
            bg=self.bg,
        )
