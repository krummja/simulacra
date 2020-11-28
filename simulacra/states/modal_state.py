from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from config import DEBUG
from state import State, T, SaveAndQuit, GameOverQuit, StateBreak

from managers.manager_service import ManagerService
from factories.factory_service import FactoryService
from views.modal_view import ModalView

if TYPE_CHECKING:
    from model import Model
    from view import View


# FIXME: By god this is messy :/
class ModalState(State[None]):
    
    NAME = "Modal"
    
    def __init__(self, model: Model, case: str) -> None:
        super().__init__()
        self._model = model
        self._case = case
        self._view = ModalView(self)
        self.result = False
        self.list_index = 0
        
        self.managers = ManagerService()
        self.managers.interface_manager.model = model
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
    
        if self._case == 'delete':
            if event.sym == tcod.event.K_y:
                self.result = True
                raise StateBreak()
            elif event.sym == tcod.event.K_n:
                self.result = False
                raise StateBreak()
        
        elif self._case == 'examine':
            area = self.model.area_data.current_area
            nearby_items = area.nearby_items
            nearby_items = [item for sublist in nearby_items for item in sublist]
            
        return super().ev_keydown(event)
    