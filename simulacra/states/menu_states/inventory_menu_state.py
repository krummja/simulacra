from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod

from state import State, StateBreak
from states.base_menu_state import BaseMenuState
from states.menu_states.item_options_state import ItemOptionsState
from views.menu_views.inventory_menu_view import InventoryMenuView

if TYPE_CHECKING:
    from components.inventory import Inventory
    from model import Model
    from view import View
    

class InventoryMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: Inventory) -> None:
        self._data = []
        self.update(data)
        super().__init__(InventoryMenuView, self._data)
    
    @property
    def data(self):
        return self._data
    
    def update(self, data: Inventory) -> None:
        if data is not None:
            _entries = [(k, v) for k, v in data['item_stacks'].items()]
            self._data = [entry[1].item for entry in _entries]
    
    def cmd_confirm(self):
        try:
            item = self._data[self.selection]
            state = ItemOptionsState(item)
            return state.loop()
        except IndexError:
            raise StateBreak()
        