from __future__ import annotations
from typing import Dict, Generic, Optional, TYPE_CHECKING

from config import *

from states import SaveAndQuit, State, T, StateBreak
from engine.actions import Action, common
from engine.model import Model
from engine.rendering import draw_main_view, draw_log
from engine.geometry import *

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

    def examine_nearby(self: ExamineState):
        area = self.model.current_area
        area.nearby_items.clear()
        for position in Point(*self.model.player.location.xy).neighbors:
            try:
                if area.items[position[0], position[1]]:
                    area.nearby_items.append(area.items[position])
            except KeyError:
                continue


class PlayerReady(AreaState["Action"]):

    def cmd_drop(self) -> Optional[Action]:
        pass

    def cmd_escape(self) -> None:
        raise SaveAndQuit()

    def cmd_examine(self) -> Optional[Action]:
        self.examine_nearby()
        state = ExamineState(self.model)
        return state.loop()

    def cmd_inventory(self) -> Optional[Action]:
        state = OverlayState(self.model)
        return state.loop()

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move(self.model.player, (x, y))

    def cmd_pickup(self) -> Action:
        pass

    def cmd_use(self) -> Optional[Action]:
        pass


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
            width=30,
            height=STAGE_PANEL_HEIGHT,
            bg=(50, 50, 50)
            )

    def on_draw(self: OverlayState, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)
        self.side_panel.on_draw(consoles)
        draw_log(self.model, consoles)

    def ev_keydown(
            self: OverlayState,
            keycode: tcod.event.KeyDown
        ) -> Optional[Action]:
        key = keycode.sym

        if key == tcod.event.K_ESCAPE:
            return self.cmd_quit()
        else:
            super().ev_keydown(keycode)

    def cmd_quit(self: OverlayState) -> Action:
        return common.Wait(self.model.player, self.model.player.location.xy)


class ExamineState(OverlayState):

    def __init__(self: ExamineState, model: Model):
        super().__init__(model)

        self.items = self.model.current_area.nearby_items
        self.symbols = "abcdefghijklmnopqrstuvwxyz"

        self.right_panel = FramePanel(
            parent=self.wrapper_panel,
            position=("center", "right"),
            width=30,
            height=len(self.items) + 4,
            bg=(50, 50, 50),
            title="nearby"
            )

    def on_draw(self: ExamineState, consoles: Dict[str, Console]) -> None:
        self.right_panel.on_draw(consoles)
        self.items = [item for sublist in self.items for item in sublist]
        for i, item in enumerate(self.items):
            sym = self.symbols[i]
            x = self.right_panel.bounds.left + 2
            y = self.right_panel.bounds.top + 2
            consoles['INTERFACE'].print(x, y + i, f"{sym}: {item.noun_text} ({item.state})")

        consoles['INTERFACE'].blit(
            dest=consoles['ROOT'],
            dest_x=self.right_panel.x,
            dest_y=self.right_panel.y,
            src_x=self.right_panel.x,
            src_y=self.right_panel.y,
            width=self.right_panel.width,
            height=self.right_panel.height
            )

    def ev_keydown(
            self: OverlayState,
            keycode: tcod.event.KeyDown
        ) -> Optional[Action]:
        key = keycode.sym
        char = None
        try:
            char = chr(key)
        except ValueError:
            pass

        if char and char in self.symbols:
            index = self.symbols.index(char)
            if index < len(self.items):
                item = self.items[index]
                return self.pick_item(item)
        return super().ev_keydown(keycode)

    def pick_item(self: ExamineState, item) -> Action:
        return common.ActivateNearby(self.model.player, item)
