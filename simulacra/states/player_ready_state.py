from __future__ import annotations
from typing import TYPE_CHECKING

from actions import common
from action import Action
from state import SaveAndQuit, StateBreak
from states.area_state import AreaState
from states.inventory_state import InventoryState
from states.modal_state import ModalState
from states.pick_location_state import PickLocationState
from views.inventory_view import InventoryView

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
        #! This could be really useful... pass in different inventory view objects
        #! depending on what I'm accessing?
        state = InventoryState(self.model, InventoryView)
        return state.loop()
    
    def cmd_examine(self):
        state = PickLocationState(self.model, "", self.model.player.location.xy)
        cursor_xy = state.loop()
        print(cursor_xy)  # TODO: Feed this into an action! :3
        # return common.Nearby.Examine(self.model.player)
    
    def cmd_pickup(self):
        return common.Nearby.Pickup(self.model.player)