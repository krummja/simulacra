from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from actions import common
from action import Action
from state import SaveAndQuit, StateBreak
from states.area_state import AreaState
from states.inventory_state import InventoryState
from states.pick_location_state import PickLocationState
from views.menu_views.inventory_menu_view import InventoryMenuView
from states.modal_states.inventory_modal_state import InventoryModalState

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
        # state = InventoryState(self.model, InventoryView)
        state = InventoryModalState(self.model)
        return state.loop()
    
    def cmd_examine(self):
        state = PickLocationState(self.model, "", self.model.player.location.xy)
        # NOTE: Ahhh, I get it now. I can assign state loops to a variable,
        # and have that state extend AreaState[<return type>].
        # On StateBreak, the loop returns the specified return type. Sick!
        # e.g.     return type       PickLocationState(AreaState[Tuple[int, int]])
        cursor_xy: Tuple[int, int] = state.loop()
        print(cursor_xy)  # TODO: Feed this into an action! :3
        # return common.Nearby.Examine(cursor_xy)
    
    def cmd_pickup(self):
        return common.Nearby.Pickup(self.model.player)
    


