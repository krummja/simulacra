from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from collections import UserList

import tcod

from state import State, StateBreak, T
from views.menu_views.inventory_menu_view import InventoryMenuView
from states.base_menu_state import BaseMenuState, ListData
from states.menu_states.item_options_state import ItemOptionsState

if TYPE_CHECKING:
    from entity import Entity
    from model import Model
    from view import View


class InventoryMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: List[Entity], state: str) -> None:
        super().__init__(InventoryMenuView, data)
        self.state = state
        self._states = {
            "inventory": None,
            "drop": None
            }
    
    def cmd_confirm(self):
        options = [_ for _ in self._data[self._selection].options.keys()]
        state = ItemOptionsState(options)
        return state.loop()