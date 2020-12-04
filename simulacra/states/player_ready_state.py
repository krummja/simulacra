from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from actions import common
from action import Action
from state import SaveAndQuit, StateBreak
from states.area_state import AreaState
from states.pick_location_state import PickLocationState
from states.menu_states.inventory_menu_state import InventoryMenuState

if TYPE_CHECKING:
    from model import Model


class PlayerReadyState(AreaState["Action"]):

    NAME = "Player Ready"

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move.Start(self.model.player, (x, y))

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
    
    def cmd_pickup(self):
        return common.Nearby.Pickup(self.model.player)
    


