from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod
from config import *

from view import View

from views.base_modal_view import BaseModalView
from views.elements.base_element import ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from state import State


class InventoryModalView(BaseModalView):
    
    def __init__(self, state: State) -> None:
        super().__init__(state, ElementConfig(
            width=30,
            height=10,
            title="INVENTORY",
            framed=True,
            ))
    
    def draw_content(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(self.x+2, self.y+2, "test")