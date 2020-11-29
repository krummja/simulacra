from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod

from state import State, StateBreak, T
from views.inventory_view import InventoryView
from states.menu_base_state import MenuBaseState

if TYPE_CHECKING:
    from view import View
    from model import Model


class InventoryState(MenuBaseState):
    
    NAME = "Inventory"
    
    def __init__(self, model: Model, view: View) -> None:
        super().__init__(model, view)
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        return super().ev_keydown(event)