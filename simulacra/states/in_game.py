from __future__ import annotations
from typing import Dict, Generic, Optional, TYPE_CHECKING

from states import SaveAndQuit, State, T
from engine.actions import Action, common
from engine.rendering import draw_main_view, draw_log

if TYPE_CHECKING:
    from tcod.console import Console


class AreaState(Generic[T], State[T]):

    def __init__(self: AreaState, model) -> None:
        super().__init__()
        self.model = model

    def on_draw(self: AreaState, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)
        draw_log(self.model, consoles)


class PlayerReady(AreaState["Action"]):

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move(self.model.player, (x, y))

    def cmd_pickup(self) -> Action:
        pass

    def cmd_inventory(self) -> Optional[Action]:
        pass

    def cmd_drop(self) -> Optional[Action]:
        pass
