from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from collections import UserList

import tcod

from state import State, StateBreak, T
from views.menu_views.inventory_menu_view import InventoryMenuView
from states.base_menu_state import BaseMenuState
from states.menu_states.item_options_state import ItemOptionsState

if TYPE_CHECKING:
    from entity import Entity
    from model import Model
    from view import View


class InventoryMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: List[Entity]) -> None:
        super().__init__(InventoryMenuView, data)
    
    def cmd_confirm(self):
        try:
            item = self._data[self.selection]
            state = ItemOptionsState(item)
            return state.loop()
        except IndexError:
            raise StateBreak()