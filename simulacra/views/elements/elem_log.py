from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

from config import *
from panel import Panel

if TYPE_CHECKING:
    from model import Model
    from model import Message
    from tcod.console import Console


class ElemLog(Panel):

    def __init__(self, model: Model) -> None:
        self.log_width = STAGE_PANEL_WIDTH
        super().__init__(**{
            'position': ('bottom', 'left'),
            'size': {'width': self.log_width,
                     'height': (CONSOLE_HEIGHT // 4)},
            'style': {'framed': True}
            })
        self.model = model

    def draw(self, consoles: Dict[str, Console]) -> None:
        # TODO: Figure out some way to color parts of strings...?
        self.on_draw(consoles)

        i = 0
        x, y = self.bounds.left + 1, self.bounds.bottom - 2
        for text in self.model.log[-2::-1]:
            i += tcod.console.get_height_rect(self.log_width, str(text))
            if i >= 10:
                break
            consoles['ROOT'].print_box(
                x, y - i, self.log_width, 0, str(text),
                fg=(100, 100, 100), bg=(0, 0, 0)
                )
        for text in self.model.log[::1]:
            consoles['ROOT'].print_box(
                x, y, self.log_width, 0, str(text) + " " * (self.log_width - len(str(text)) - 2),
                fg=(255, 255, 255), bg=(0, 0, 0)
                )