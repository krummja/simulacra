from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from config import DEBUG
from state import State, T, SaveAndQuit, GameOverQuit, StateBreak

from actions import common
from managers.manager_service import ManagerService
from factories.factory_service import FactoryService
from views.modal_view import ModalView
from views.stage_view import StageView

if TYPE_CHECKING:
    from item import Item
    from model import Model
    from view import View


# REFACTOR: DEPRECATE
class ModalState(State[None]):
    
    NAME = "Modal"
    
    def __init__(self, model: Model, case: str) -> None:
        super().__init__()
        self._model = model
        self._case = case
        self._view = ModalView(self)
        self._stage_view = StageView(self, self.model)
        self.result = False
        self.list_index = 0
        self.list_functions = []
        
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
            
            if event.sym in self.MOVE_KEYS:
                self.list_index += self.MOVE_KEYS[event.sym][1]
                if self.list_index < 0:
                    self.list_index = 0
                if self.list_index >= len(self.get_nearby_items_list()):
                    self.list_index = len(self.get_nearby_items_list()) - 1
            
            if event.sym == tcod.event.K_RETURN:
                if len(self.get_nearby_items_list()) > 0:
                    if state.result:
                        raise StateBreak()
                else:
                    pass
                
        elif self._case == 'options':
            
            if event.sym in self.MOVE_KEYS:
                self.list_index += self.MOVE_KEYS[event.sym][1]
                if self.list_index < 0:
                    self.list_index = 0
                if self.list_index >= len(self._view._opt_list):
                    self.list_index = len(self._view._opt_list) - 1

            if event.sym == tcod.event.K_RETURN:
                self.result = True
                raise StateBreak()
   
            if event.sym == tcod.event.K_ESCAPE:
                raise StateBreak()
            
        return super().ev_keydown(event)
   
    def get_nearby_items_list(self) -> List[Item]:
        """Grab each adjacent tile's list of items and flatten into one list.
        Returns a single list containing all of the adjacent items.
        """
        self.model.area_data.current_area.item_model.get_nearby()
        nearby_items = self._model.nearby_items
        nearby_items = [item for subl in nearby_items for item in subl]
        return nearby_items
    
    def get_component_list(self, target_item: Item):
        """For a specified target item, return that item's list of 
        components.
        """
        component_list = []
        for component in target_item.components.items():
            component_list.append(component)
        return component_list
        
    def populate_view_list(self, list_items):
        options = []
        functions = []
        for item in list_items:
            options.append(item[0])
            functions.append(item[1])
        self._view._opt_list = options
        self.list_functions = functions