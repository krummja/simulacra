from __future__ import annotations  # type: ignore
from typing import Any, Dict, Generic, Optional, TypeVar, TYPE_CHECKING, Tuple

import tcod
import tcod.console as Console

from engine.actions import Action
from engine.actions import common
from engine.rendering import *
from . import State, StateBreak

if TYPE_CHECKING:
    import tcod.console as Console
    from engine.model import Model
    from engine.item import Item

T = TypeVar("T")


class AreaState(Generic[T], State[T]):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)


class PlayerReady(AreaState["Action"]):
    
    def cmd_escape(self) -> None:
        raise SystemExit()

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move(self.model.player, (x, y))

    def cmd_pickup(self) -> Action:
        pass

    def cmd_inventory(self) -> Optional[Action]:
        pass

    def cmd_drop(self) -> Optional[Action]:
        pass


class BaseInventoryMenu(AreaState["Action"]):
    pass


class UseInventory(BaseInventoryMenu):
    pass


class DropInventory(BaseInventoryMenu):
    pass


class PickLocation(AreaState[Tuple[int, int]]):
    pass