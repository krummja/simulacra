from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod
from config import *
from tiles.font_map import font_map

from views.menu_base_view import MenuBaseView

if TYPE_CHECKING:
    from tcod.console import Console
    from state import State


class InventoryView(MenuBaseView):
    
    def __init__(self, state: State) -> None:
        super().__init__(state)
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].draw_frame(
            x=0, y=0, width=CONSOLE_WIDTH, height=CONSOLE_HEIGHT,
            fg=(255, 255, 255), bg=(0, 0, 0)
            )