from __future__ import annotations
from typing import Dict, List, TYPE_CHECKING

from config import *
from panel import Panel

if TYPE_CHECKING:
    from tcod.console import Console


class ElemHelpText(Panel):

    def __init__(self, content: List[str]) -> None:
        super().__init__(**{
            'position': ('bottom', 'center'),
            'size': {'width': CONSOLE_WIDTH, 'height': 3},
            })
        self.content = content

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.on_draw(consoles)

        help_text = ""
        for item in self.content:
            help_text += item

        text_width = len(help_text)
        consoles['ROOT'].print(
            (self.size_width - text_width) // 2,
            self.y + 1,
            help_text,
            fg=self.style_fg,
            bg=self.style_bg
            )
