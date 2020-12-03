from __future__ import annotations
from typing import TYPE_CHECKING

import tcod

from state import StateBreak
from views.modal_views.confirm_modal_view import ConfirmModalView
from states.base_modal_state import BaseModalState
    

class ConfirmModalState(BaseModalState[bool]):
    
    def __init__(self, model: Model) -> None:
        super().__init__(model, ConfirmModalView)
        self.result = False
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> bool:
        if event.sym == tcod.event.K_y:
            self.result = True
            raise StateBreak()
        elif event.sym == tcod.event.K_n:
            raise StateBreak()
        return super().ev_keydown(event)
    
    def cmd_quit(self) -> None:
        raise StateBreak()