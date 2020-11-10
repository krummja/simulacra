from __future__ import annotations
from typing import TYPE_CHECKING

from actions import common
from action import Action
from state import SaveAndQuit, StateBreak
from states.area_state import AreaState


class PlayerReadyState(AreaState["Action"]):

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move.Start(self.model.player, (x, y))

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_quit(self) -> None:
        raise StateBreak()
