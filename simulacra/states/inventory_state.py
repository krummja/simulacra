from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod

from state import State, StateBreak, T
from states.base_menu_state import BaseMenuState
from states.area_state import AreaState

if TYPE_CHECKING:
    from view import View
    from model import Model


class InventoryState(BaseMenuState):
    
    NAME = "Inventory"
    
    def __init__(self, model: Model, view: View) -> None:
        super().__init__(model, view)
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        return super().ev_keydown(event)