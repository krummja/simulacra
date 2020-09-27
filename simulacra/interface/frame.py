from __future__ import annotations  # type: ignore
from typing import Dict, Optional, TYPE_CHECKING, Tuple

from constants import *
from consoles import *
from interface.panel import Panel

if TYPE_CHECKING:
    import tcod.console as Console


class FramePanel(Panel):
    
    def __init__(
            self,
            position: Optional[Tuple[str, str]]=None,
            parent: Panel=None,
            width: int=CONSOLE_WIDTH,
            height: int=0,
            margin: int=0,
            vertical_offset: int=0,
            horizontal_offset: int=0,
            fg: Tuple[int, int, int]=(255, 255, 255),
            bg: Tuple[int, int, int]=(0, 0, 0),
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

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].draw_frame(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height
        )