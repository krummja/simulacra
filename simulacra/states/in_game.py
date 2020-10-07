from __future__ import annotations
from typing import Generic, Optional, TYPE_CHECKING

from config import *

from states import SaveAndQuit, State, StateBreak, T
from engine.actions import Action, common
from engine.rendering import draw_main_view, draw_log
from engine.geometry import *

from interface.panel import Panel
from interface.frame_panel import FramePanel

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.items import Item
    from engine.model import Model


class AreaState(Generic[T], State[T]):

    def __init__(self: AreaState, model: Model) -> None:
        super().__init__()
        self.model = model

        self.side_panel = FramePanel(
            position=("top", "right"),
            width=SIDE_PANEL_WIDTH,
            height=SIDE_PANEL_HEIGHT,
            bg=(0, 0, 0)
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

    def cmd_equipment(self) -> Optional[Action]:
        state = BaseEquipmentMenu(self.model)
        return state.loop()

    def cmd_inventory(self) -> Optional[Action]:
        state = UseInventory(self.model)
        return state.loop()

    def cmd_move(self, x: int, y: int) -> Action:
        return common.Move(self.model.player.components['ACTOR'], (x, y))

    def cmd_pickup(self) -> Action:
        return common.Pickup(self.model.player.components['ACTOR'])

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
            event: tcod.event.KeyDown
        ) -> Optional[Action]:
        key = event.sym

        if key == tcod.event.K_ESCAPE:
            return self.cmd_escape()
        else:
            super().ev_keydown(event)

    def cmd_escape(self: OverlayState):
        return common.Wait(self.model.player.components['ACTOR'])


class ExamineState(OverlayState):

    def __init__(self: ExamineState, model: Model):
        super().__init__(model)

        self.items = self.model.current_area.nearby_items
        self.at_feet = self.model.current_area
        self.symbols = "abcdefghijklmnopqrstuvwxyz"

        self.right_panel = FramePanel(
            parent=self.wrapper_panel,
            position=("center", "right"),
            width=28,
            height=len(self.items) + 4,
            bg=(0, 0, 0),
            title="nearby"
            )

    def on_draw(self: ExamineState, consoles: Dict[str, Console]) -> None:
        self.right_panel.on_draw(consoles)
        self.items = [item for sublist in self.items for item in sublist]

        for i, item in enumerate(self.items):
            sym = self.symbols[i]
            x = self.right_panel.bounds.left + 2
            y = self.right_panel.bounds.top + 2
            consoles['INTERFACE'].print(x, y + i, f"{sym}: {item.noun_text} {item.suffix}")

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
            event: tcod.event.KeyDown
        ) -> Optional[Action]:
        key = event.sym
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
        return super().ev_keydown(event)

    def pick_item(self: ExamineState, item) -> Action:
        return common.ActivateNearby(self.model.player.components['ACTOR'], item)


class BaseEquipmentMenu(OverlayState):

    def __init__(self: BaseEquipmentMenu, model: Model) -> None:
        super().__init__(model)

        self.equipment = self.model.player.components['EQUIPMENT']
        self.left_panel = FramePanel(
            parent=self.wrapper_panel,
            position=("top", "left"),
            width=(STAGE_PANEL_WIDTH // 2) - 2,
            height=STAGE_PANEL_HEIGHT,
            bg=(0, 0, 0),
            title=" equipment "
            )

        self.inventory = self.model.player.components['INVENTORY']
        self.right_panel = FramePanel(
            parent=self.wrapper_panel,
            position=("top", "right"),
            width=(STAGE_PANEL_WIDTH // 2) - 2,
            height=STAGE_PANEL_HEIGHT,
            bg=(0, 0, 0),
            title=" inventory "
            )

    def on_draw(self: BaseEquipmentMenu, consoles: Dict[str, Console]) -> None:
        self.left_panel.on_draw(consoles)
        self.right_panel.on_draw(consoles)

        # for i, item in enumerate(self.equipment.contents):
        #
        #     sym = self.equipment.symbols[i]
        #     x = self.left_panel.bounds.left + 2
        #     y = self.left_panel.bounds.top + 2
        #     consoles['INTERFACE'].print(x, y + i, f"{sym}: {item}")

        # Enumerate Inventory Contents
        # FIXME: The inventory contents don't show up.
        # TODO: Make it so that inventory only appears when an equipment slot
        # TODO: ... is selected.
        for i, item in enumerate(self.inventory.contents):
            sym = self.inventory.symbols[i]
            x = self.right_panel.bounds.left + 2
            y = self.right_panel.bounds.top + 2
            consoles['INTERFACE'].print(x, y + i, f"{sym}: {chr(item.char)}   {item.noun_text}")

    def ev_keydown(self: BaseEquipmentMenu, event: tcod.event.KeyDown) -> Optional[Action]:
        char: Optional[str] = None
        try:
            char = chr(event.sym)
        except ValueError:
            pass
        # if char and char in self.equipment.symbols:
        #     index = self.equipment.symbols.index(char)
        #     if index < len(self.equipment.contents):
        #         item = self.equipment.contents[index]
        #         return self.pick_item(item)
        return super().ev_keydown(event)

    def pick_item(self: BaseEquipmentMenu, item: Item) -> Optional[Action]:
        raise NotImplementedError()


class BaseInventoryMenu(OverlayState):

    def __init__(self: BaseInventoryMenu, model: Model) -> None:
        super().__init__(model)

        self.inventory = self.model.player.components['INVENTORY']
        self.right_panel = FramePanel(
            parent=self.wrapper_panel,
            position=("top", "right"),
            width=(STAGE_PANEL_WIDTH // 2) - 2,
            height=STAGE_PANEL_HEIGHT,
            bg=(0, 0, 0),
            title=" inventory "
            )

    def on_draw(self: BaseInventoryMenu, consoles: Dict[str, Console]) -> None:
        self.right_panel.on_draw(consoles)

        for i, item in enumerate(self.inventory.contents):
            sym = self.inventory.symbols[i]
            x = self.right_panel.bounds.left + 2
            y = self.right_panel.bounds.top + 2
            consoles['INTERFACE'].print(x, y + i, f"{sym}: {chr(item.char)}   {item.noun_text}")

        consoles['INTERFACE'].blit(
            dest=consoles['ROOT'],
            dest_x=self.right_panel.x,
            dest_y=self.right_panel.y,
            src_x=self.right_panel.x,
            src_y=self.right_panel.y,
            width=self.right_panel.width,
            height=self.right_panel.height
            )

    def ev_keydown(self: BaseInventoryMenu, event: tcod.event.KeyDown) -> Optional[Action]:
        char: Optional[str] = None
        try:
            char = chr(event.sym)
        except ValueError:
            pass
        if char and char in self.inventory.symbols:
            index = self.inventory.symbols.index(char)
            if index < len(self.inventory.contents):
                item = self.inventory.contents[index]
                return self.pick_item(item)
        return super().ev_keydown(event)

    def pick_item(self: BaseInventoryMenu, item: Item) -> Optional[Action]:
        raise NotImplementedError()


class UseInventory(BaseInventoryMenu):
    def pick_item(self: UseInventory, item: Item) -> Action:
        return common.ActivateItem(self.model.player.components['ACTOR'], item)
