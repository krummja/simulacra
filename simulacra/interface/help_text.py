from __future__ import annotations
from typing import List, TYPE_CHECKING, Tuple

from config import *
from interface.panel import Panel

if TYPE_CHECKING:
    import tcod.console as Console


class HelpText(Panel):

    def __init__(
            self,
            position=("bottom", "center"),
            parent: Panel = None,
            width: int = CONSOLE_WIDTH,
            height: int = 1,
            margin: int = 1,
            vertical_offset: int = 0,
            horizontal_offset: int = 0,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (0, 0, 0),
            content: List[str] = []
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
        self.content = content

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        help_text = ""
        for item in self.content:
            help_text += item

        text_width = len(help_text)
        consoles['ROOT'].print(
            (self.width - text_width) // 2,
            self.y,
            help_text,
            fg=self.fg,
            bg=self.bg
            )
