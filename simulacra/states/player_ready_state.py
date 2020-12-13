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
from states.menu_states.inventory_menu_state import InventoryMenuState
from states.effects_state import EffectsState
from particles.test_effect import TestEffect

if TYPE_CHECKING:
    from model import Model


class PlayerReadyState(Generic[T], AreaState[T]):

    NAME = "Player Ready"

    def __init__(self, model: Model) -> None:
        super().__init__(model)
        self.result_manager = ResultManager(self.model, self)

    def cmd_move(self, x: int, y: int) -> Action:
        action = common.Move.Start(self.model.player, (x, y))
        action.success = True
        result = action.make_result(action)
        self.result_manager.add_result(result)
        return action

    def cmd_escape(self) -> None:
        if self.suspend:
            self.suspend = False
        else:
            raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak("PlayerReadyState")

    def cmd_inventory(self):
        state = InventoryMenuState(
            self.manager_service.data_manager.query(
                entity="PLAYER", 
                component="INVENTORY", 
                key="contents"
                ), "inventory")
        return state.loop()
    
    def cmd_examine(self):
        state = PickLocationState(self.model, "", self.model.player.location.xy)
        cursor_xy: Tuple[int, int] = state.loop()
    
    def cmd_equipment(self):
        # self.suspend = True
        state = EffectsState(self.model)
        state.loop()
    
    def cmd_pickup(self):
        return common.Nearby.Pickup(self.model.player)
    
    def cmd_drop(self):
        state = InventoryMenuState(
            self.manager_service.data_manager.query(
                entity="PLAYER",
                component="INVENTORY",
                key="contents"
            ), "drop")
        return state.loop()