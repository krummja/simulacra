from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod

from .state import State, StateBreak
from .base_menu_state import BaseMenuState
from .item_options_state import ItemOptionsState
from interface.views.inventory_menu_view import InventoryMenuView

if TYPE_CHECKING:
    from engine.components import Inventory
    from engine.model import Model
    from interface import View


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
