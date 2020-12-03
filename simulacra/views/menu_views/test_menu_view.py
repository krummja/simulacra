from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import tcod
from config import *

from view import View
from views.elements.base_element import BaseElement, ElementConfig
from views.base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from entity import Entity
    from tcod.console import Console
    from state import State


class TestMenuView(BaseMenuView):
    
    def __init__(self, state: State) -> None:
        super().__init__(state, ElementConfig(
            position=("top", "left"),
            width=30, height=20,
            fg=(255, 255, 255),
            framed=True
            ))