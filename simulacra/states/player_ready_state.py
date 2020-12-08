from __future__ import annotations
from typing import Generic, Tuple, TYPE_CHECKING

from actions import common
from action import Action
from result import Result
from state import SaveAndQuit, StateBreak, T
from states.area_state import AreaState
from states.pick_location_state import PickLocationState
from states.menu_states.inventory_menu_state import InventoryMenuState
# from states.effects_state import EffectsState

if TYPE_CHECKING:
    from model import Model


class PlayerReadyState(Generic[T], AreaState[T]):

    NAME = "Player Ready"
    
    def __init__(self, model: Model) -> None:
        super().__init__(model)
        self.model.result_manager.state = self

    # def play_effect(self):
    #     state = EffectsState(self.model)
    #     state.loop()

    def cmd_move(self, x: int, y: int) -> Action:
        action = common.Move.Start(self.model.player, (x, y))
        action.success = True
        action.make_result(action)
        return action

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak()

    def cmd_inventory(self):
        state = InventoryMenuState(
            self.manager_service.data_manager.query(
                entity="PLAYER", 
                component="INVENTORY", 
                key="contents"
                ))
        return state.loop()
    
    def cmd_examine(self):
        state = PickLocationState(self.model, "", self.model.player.location.xy)
        cursor_xy: Tuple[int, int] = state.loop()
    
    def cmd_equipment(self):
        state = EffectsState(self.model)
        state.loop()
    
    def cmd_pickup(self):
        return common.Nearby.Pickup(self.model.player)