from __future__ import annotations
from typing import Optional, TYPE_CHECKING
 
from state import State, StateBreak
from views.menu_views.equipment_menu_view import EquipmentMenuView
from states.base_menu_state import BaseMenuState
from states.menu_states.item_options_state import ItemOptionsState
 
if TYPE_CHECKING:
     from components.equipment import Equipment
     from entity import Entity
     from model import Model
     from view import View


class EquipmentMenuState(BaseMenuState["Action"]):
    
    def __init__(self, data: Equipment) -> None:
        self._data = []
        self.update(data)
        super().__init__(EquipmentMenuView, self._data)

    def update(self, data: Equipment) -> None:
        if data is not None:
            self._entries = [(k, v) for k, v in data.items()]
            self._data = [entry[1]['slot'] for entry in self._entries]
    
    def cmd_confirm(self):
        try:
            item = self._data[self.selection]
            state = ItemOptionsState(item)
            return state.loop()
        except IndexError:
            raise StateBreak()