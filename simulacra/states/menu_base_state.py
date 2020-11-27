from __future__ import annotations
from typing import Optional, TYPE_CHECKING

import tcod

from state import State, StateBreak, T
from views.menu_base_view import MenuBaseView

if TYPE_CHECKING:
    from model import Model
    from view import View


class MenuBaseState(State[None]):
    
    def __init__(self, model: Model, view: View) -> None:
        super().__init__()
        self._model = model
        self._view = view(self)
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        return super().ev_keydown(event)