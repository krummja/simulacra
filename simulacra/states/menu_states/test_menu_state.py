from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from collections import UserList

import tcod

from state import State, StateBreak, T
from views.menu_views.test_menu_view import TestMenuView
from states.base_menu_state import BaseMenuState, ListData

if TYPE_CHECKING:
    from entity import Entity
    from model import Model
    from view import View


class TestMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: List[Entity]) -> None:
        super().__init__(TestMenuView, data)
        
