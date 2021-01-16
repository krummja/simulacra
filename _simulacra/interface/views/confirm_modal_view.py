from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod
from config import *

from interface.views.view import View

from .base_modal_view import BaseModalView
from interface.elements.base_element import ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.states.state import State


class ConfirmModalView(BaseModalView):

    def __init__(self, state: State) -> None:
        super().__init__(state, ElementConfig(
            position=("center", "center"),
            width=27,
            height=7,
            offset_y=12,
            title="DELETE",
            framed=True,
            fg=(255, 0, 0)
            ))

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        r, g, b = 255, 0, 0
        set_fg = f"{tcod.COLCTRL_FORE_RGB:c}{r:c}{g:c}{b:c}"
        reset = f"{tcod.COLCTRL_STOP:c}"
        consoles['ROOT'].print(
            self.content.left+1, self.content.top+1,
            f"this is {set_fg}IRREVERSIBLE{reset}!\n \nare you sure? (y/n/esc)",
            fg=(255, 255, 255)
            )
