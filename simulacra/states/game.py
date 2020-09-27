from __future__ import annotations  # type: ignore
from typing import Any, Dict, Generic, Optional, TypeVar, TYPE_CHECKING, Tuple

import tcod
import tcod.console as Console

from constants import *
from interface.panel import Panel
from interface.frame import FramePanel
from interface.gauge import Gauge
from engine.actions import Action
from engine.actions import common
from engine.rendering import *
from engine.hues import *
from . import State, StateBreak, GameOverQuit, SaveAndQuit

if TYPE_CHECKING:
    import tcod.console as Console
    from engine.model import Model
    from engine.items import Item

T = TypeVar("T")


class AreaState(Generic[T], State[T]):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

        self.side_panel = FramePanel(
            position = ("top", "right"),
            width = SIDE_PANEL_WIDTH,
            height = SIDE_PANEL_HEIGHT,
            bg=(50, 50, 50)
        )

        self.health_bar = Gauge(
            x=CONSOLE_WIDTH - SIDE_PANEL_WIDTH + 2,
            y=6, 
            width=SIDE_PANEL_WIDTH-4, 
            text=f"HP: {self.model.player.character.attributes['health']}", 
            fullness=self.model.player.character.attributes['health'].current_over_base, 
            fg=COLOR['red'], 
            bg=COLOR['nero']
        )

        self.energy_bar = Gauge(
            x=CONSOLE_WIDTH - SIDE_PANEL_WIDTH + 2,
            y=8, 
            width=SIDE_PANEL_WIDTH-4,
            text=f"EP: {self.model.player.character.attributes['energy']}", 
            fullness=self.model.player.character.attributes['energy'].current_over_base, 
            fg=COLOR['steel blue'], 
            bg=COLOR['nero']
        )

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)
        self.side_panel.on_draw(consoles)
        draw_log(self.model, consoles)

        consoles['ROOT'].print(
            0, 0, str(self.model.player.location.xy), fg=(255, 255, 255)
        )

        self.health_bar.on_draw(consoles)
        self.energy_bar.on_draw(consoles)

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


class GameOver(AreaState[None]):

    def cmd_quit(self) -> None:
        """Save and quit."""
        raise SystemExit()

    def cmd_escape(self) -> None:
        """Finish game."""
        raise GameOverQuit()


class BaseInventoryMenu(AreaState["Action"]):
    pass


class UseInventory(BaseInventoryMenu):
    pass


class DropInventory(BaseInventoryMenu):
    pass


class PickLocation(AreaState[Tuple[int, int]]):
    pass

