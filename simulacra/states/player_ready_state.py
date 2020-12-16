from __future__ import annotations
from typing import Generic, Tuple, TYPE_CHECKING

from config import *

from managers.result_manager import ResultManager
from actions import common
from action import Action
from result import Result
from state import SaveAndQuit, StateBreak, T
from states.area_state import AreaState
from states.pick_location_state import PickLocationState
from states.effects_state import EffectsState
from particles.test_effect import TestEffect

if TYPE_CHECKING:
    from model import Model


class PlayerReadyState(Generic[T], AreaState[T]):

    NAME = "Player Ready"

    def __init__(self, model: Model) -> None:
        super().__init__(model)

    def cmd_move(self, x: int, y: int) -> Action:
        action = common.Move.Start(self.model.player, (x, y))
        action.success = True
        result = action.make_result(action)
        self.manager_service.result_manager.add_result(result)
        return action

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak("PlayerReadyState")

    def cmd_inventory(self):
        pass
        # inventory_data = self.manager_service.data_manager.query(
        #     entity="PLAYER", 
        #     component="INVENTORY")
        # state = InventoryMenuState(inventory_data)
        # return state.loop()
        # self._view.inventory_panel.update(inventory_data)
    
    
    def cmd_examine(self):
        state = PickLocationState(self.model, "", self.model.player.location.xy)
        cursor_xy: Tuple[int, int] = state.loop()
    
    def cmd_equipment(self):
        pass
        # equipment_data = self.manager_service.data_manager.query(
        #         entity="PLAYER",
        #         component="EQUIPMENT")
        # state = EquipmentMenuState(equipment_data)
        # return state.loop()
        # self._view.equipment_panel.update(equipment_data)
    
    def cmd_pickup(self):
        return common.Nearby.Pickup(self.model.player)

    def cmd_debug_1(self):
        data = self.manager_service.data_manager.query(
            entity="PLAYER",
            component="INVENTORY")
        for item in data.values():
            print(repr(item['slot']))        
    
    def cmd_debug_2(self):
        print(self._view.inventory_panel.data)
    
    def cmd_debug_3(self):
        print("F3")
    
    def cmd_debug_4(self):
        print("F4")