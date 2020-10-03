from __future__ import annotations
from typing import Dict, Generic, Optional, TYPE_CHECKING

from config import *

from states import SaveAndQuit, State, T, StateBreak
from engine.actions import Action, common
from engine.model import Model
from engine.rendering import draw_main_view, draw_log, refresh

from interface.panel import Panel
from interface.frame_panel import FramePanel

if TYPE_CHECKING:
    from tcod.console import Console


class AreaState(Generic[T], State[T]):

    def __init__(self: AreaState, model: Model) -> None:
        super().__init__()
        self.model = model

        self.side_panel = FramePanel(
            position=("top", "right"),
            width=SIDE_PANEL_WIDTH,
            height=SIDE_PANEL_HEIGHT,
            bg=(50, 50, 50)
            )

    def on_draw(self: AreaState, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)
        self.side_panel.on_draw(consoles)
        draw_log(self.model, consoles)


class PlayerReady(AreaState["Action"]):

    def cmd_drop(self) -> Optional[Action]:
        pass

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_examine(self) -> Optional[Action]:
        return common.ExamineNearby(self.model.player)

    def cmd_inventory(self) -> Optional[Action]:
        state = OverlayState(self.model)
        return state.loop()

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move(self.model.player, (x, y))

    def cmd_pickup(self) -> Action:
        pass

    def cmd_use(self) -> Optional[Action]:
        pass


# FIXME: StateBreak doesn't seem to clear the console correctly...
class OverlayState(AreaState["Action"]):

    def __init__(self: OverlayState, model: Model) -> None:
        super().__init__(model)

        self.wrapper_panel = Panel(
            position=("top", "left"),
            width=STAGE_PANEL_WIDTH,
            height=STAGE_PANEL_HEIGHT,
            )

        self.right_panel = FramePanel(
            parent=self.wrapper_panel,
            position=("top", "right"),
            width=20,
            height=STAGE_PANEL_HEIGHT,
            bg=(50, 50, 50)
            )

    def on_draw(self: OverlayState, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)
        self.right_panel.on_draw(consoles)

    def ev_keydown(
            self: OverlayState,
            keycode: tcod.event.KeyDown
        ) -> Optional[Action]:
        key = keycode.sym

        if key == tcod.event.K_ESCAPE:
            self.cmd_quit()

    def cmd_quit(self: OverlayState) -> None:
        CONSOLES['ROOT'].clear()
        raise StateBreak()
