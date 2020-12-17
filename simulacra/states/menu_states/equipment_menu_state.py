from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from state import StateBreak
from states.base_menu_state import BaseMenuState
from states.menu_states.item_options_state import ItemOptionsState
from views.menu_views.equipment_menu_view import EquipmentMenuView

if TYPE_CHECKING:
    from components.equipment import Equipment


class EquipmentMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: Equipment) -> None:
        self._data = []
        self.update(data)
        super().__init__(EquipmentMenuView, self._data)

    def update(self, data: Equipment) -> None:
        if data is not None:
            _slots = [(k, v) for k, v in data.items()]
            self._data = [slot[1] for slot in _slots]
        
    def cmd_confirm(self):
        try:
            item = self._data[self.selection].item
            state = ItemOptionsState(item)
            return state.loop()
        except AttributeError:
            raise StateBreak()