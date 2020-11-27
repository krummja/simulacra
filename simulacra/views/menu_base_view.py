from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from view import View

if TYPE_CHECKING:
    from tcod.console import Console
    from state import State


class MenuBaseView(View):
    
    def __init__(self, state: State) -> None:
        super().__init__(state)
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        pass