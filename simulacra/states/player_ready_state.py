from __future__ import annotations
from typing import TYPE_CHECKING

from actions import common
from action import Action
from state import SaveAndQuit, StateBreak
from states.area_state import AreaState
from states.inventory_state import InventoryState
from views.inventory_view import InventoryView

if TYPE_CHECKING:
    from model import Model


class PlayerReadyState(AreaState["Action"]):

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move.Start(self.model.player, (x, y))

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak()

    def cmd_inventory(self):
        state = InventoryState(self.model, InventoryView)
        return state.loop()