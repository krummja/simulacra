from __future__ import annotations  # type: ignore
from typing import Any, Dict, Generic, Optional, TypeVar, TYPE_CHECKING, Tuple

import tcod
import tcod.console as Console

from constants import *
from interface.panel import Panel
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
        interface_test(consoles)


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


def interface_test(consoles: Dict[Console]):
    
    right_panel_width = 30
    right_panel_height = CONSOLE_HEIGHT

    right_panel = Panel(
        position=("center", "right"),
        width=right_panel_width,
        height=right_panel_height,
        bg=(40, 40, 40)
    )
    right_panel.on_draw(consoles)

    Panel(position=("top", "left"),
          parent=right_panel,
          width=28,
          height=10,
          margin=1,
          bg=(100, 40, 40)).on_draw(consoles)

    Panel(position=("top", "left"),
          parent=right_panel,
          width=10,
          height=10,
          margin=1,
          vertical_offset=11,
          bg=(100, 100, 40)).on_draw(consoles)

    Panel(position=("bottom", "right"),
          parent=right_panel,
          width=14,
          height=10,
          margin=1,
        #   vertical_offset=11,
          bg=(100, 40, 100)).on_draw(consoles)

    Panel(position=("top", "right"),
          parent=right_panel,
          width=17,
          height=20,
          margin=1,
          vertical_offset=11,
          bg=(200, 0, 200)).on_draw(consoles)