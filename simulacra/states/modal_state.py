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


class ModalState(State[None]):
    
    def __init__(self, model: Model, sort: str) -> None:
        super().__init__()
        self._model = model
        self._sort = sort
        self._view = ModalView(self)
        self.result = False
        self.list_index = 0
        
        self.managers = ManagerService()
        self.managers.interface_manager.model = model
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
    
        if self._sort == 'delete':
            if event.sym == tcod.event.K_y:
                self.result = True
                raise StateBreak()
            elif event.sym == tcod.event.K_n:
                self.result = False
                raise StateBreak()
        
        elif self._sort == 'examine':
            area = self.model.area_data.current_area
            nearby_items = area.nearby_items
            nearby_items = [item for sublist in nearby_items for item in sublist]
            print(self.managers.interface_manager.container_items(*self.model.player.location.xy))
            
            
        return super().ev_keydown(event)
    