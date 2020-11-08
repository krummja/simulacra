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
            'style': {'fg': (255, 255, 255), 'framed': True}
            })
        self.content = content

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        help_text = ""
        for item in self.content:
            help_text += item

        text_width = len(help_text)
        consoles['ROOT'].print(
            (self.width - text_width) // 2,
            self.y - 2,
            help_text,
            fg=self.fg,
            bg=self.bg
            )
