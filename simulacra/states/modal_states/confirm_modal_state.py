from __future__ import annotations
from typing import TYPE_CHECKING

from views.modal_views.inventory_modal_view import InventoryModalView
from states.base_modal_state import BaseModalState
    

class ConfirmModalState(BaseModalState[bool]):
    
    def __init__(self, model: Model) -> None:
        super().__init__(model, InventoryModalView)