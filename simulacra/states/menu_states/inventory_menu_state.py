from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from collections import UserList

import tcod

from state import State, StateBreak, T
from views.menu_views.inventory_menu_view import InventoryMenuView
from states.base_menu_state import BaseMenuState
from states.menu_states.item_options_state import ItemOptionsState

if TYPE_CHECKING:
    from components.inventory import Inventory
    from entity import Entity
    from model import Model
    from view import View


class InventoryMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: Inventory) -> None:
        self._data = []
        if data is not None:
            self._entries = [(k, v) for k, v in data.items()]
            self._data = [entry[1]['slot'] for entry in self._entries]
        super().__init__(InventoryMenuView, self._data)
    
    def cmd_confirm(self):
        try:
            item = self._data[self.selection]
            state = ItemOptionsState(item)
            return state.loop()
        except IndexError:
            raise StateBreak()