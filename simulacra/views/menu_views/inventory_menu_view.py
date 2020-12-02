from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional

import tcod
from config import *
from tiles.font_map import font_map

from views.base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from state import State
    from tcod.console import Console


# REFACTOR
class InventoryMenuView(BaseMenuView):
    
    def __init__(self, state: State) -> None:
        super().__init__(state)
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        super().draw(consoles)
        consoles['ROOT'].draw_frame(
            x=10, y=10, width=CONSOLE_WIDTH - 20, height=CONSOLE_HEIGHT - 20,
            fg=(255, 255, 255), bg=(0, 0, 0)
            )
        consoles['ROOT'].print(12, 12, "Hello, world!")
