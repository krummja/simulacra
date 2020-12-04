from __future__ import annotations
from typing import Generic, Optional, TYPE_CHECKING

import tcod

from state import State, StateBreak, T
from states.area_state import AreaState
from views.base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from model import Model
    from view import View


class BaseModalState(Generic[T], State[T]):
    """Menu state that partially obscures the main game view."""
    
    NAME = "Modal Base"
    
    def __init__(self, model: Model, view: View) -> None:
        super().__init__()
        self._model = model
        self._view = view(self)
        
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        return super().ev_keydown(event)
        