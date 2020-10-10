from __future__ import annotations
from typing import Generic, Optional, TYPE_CHECKING

from config import *

from states import SaveAndQuit, State, StateBreak, T
from engine.actions import Action, common, Impossible
from engine.rendering import draw_main_view, draw_log
from engine.geometry import *

from interface.panel import Panel
from interface.frame_panel import FramePanel
from interface.inventory import InventoryPanel
from interface.equipment import EquipmentPanel


if TYPE_CHECKING:
    from tcod.console import Console
    from engine.items import Item
    from engine.model import Model


container_manager = ContainerManager()


class AreaState(Generic[T], State[T]):
    """The base State for the currently active area.
    """

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


class PlayerReady(AreaState["Action"]):

    def cmd_move(self, x: int, y: int) -> Action:
        """Move the player."""
        return common.Move(self.model.player.components['ACTOR'], (x, y))

    def cmd_drop(self) -> Optional[Action]:
        """Drop an item from inventory."""
        state = DropInventory(self.model)
        return state.loop()

    def cmd_pickup(self) -> Action:
        """Pick up an item at the player's position."""
        return common.Pickup(self.model.player.components['ACTOR'])

    def cmd_examine(self) -> Optional[Action]:
        """Examine whatever is in the tiles around the player."""
        self.model.current_area.examine_nearby()
        state = ExamineItemMenu(self.model)
        return state.loop()

    def cmd_equipment(self) -> Optional[Action]:
        """Raise the Equipment menu."""
        state = BaseEquipmentMenu(self.model)
        return state.loop()

    def cmd_inventory(self) -> Optional[Action]:
        """Raise the Inventory menu."""
        state = UseInventory(self.model)
        return state.loop()

    def cmd_escape(self) -> None:
        """Return to the main menu."""
        raise SaveAndQuit()

    def cmd_quit(self: BaseMenuOverlay) -> None:
        """Return to previous state."""
        raise StateBreak()


class BaseMenuOverlay(AreaState["Action"]):
    """Pause the current area state and open an overlay to which interface
    elements can be rendered.
    """

    def __init__(self: BaseMenuOverlay, model: Model) -> None:
        super().__init__(model)
        self.wrapper_panel = Panel(
            position=("top", "left"),
            width=STAGE_PANEL_WIDTH, height=STAGE_PANEL_HEIGHT,
            )
        self.right_panel = FramePanel(
            parent=self.wrapper_panel, position=("top", "right"),
            width=30, height=STAGE_PANEL_HEIGHT,
            bg=(50, 50, 50)
            )


class BaseExamineMenu(BaseMenuOverlay):
    # TODO: Make this more general so that it can be extended by various
    # TODO: ... different examine menu states.

    option_list: List[str] = []

    def __init__(self: BaseExamineMenu, model: Model):
        super().__init__(model)
        self.symbols = "abcdefghijklmnopqrstuvwxyz"
        self.items = self.model.current_area.nearby_items
        self.items = [item for sublist in self.items for item in sublist]
        self.right_panel = FramePanel(
            parent=self.wrapper_panel, position=("center", "right"),
            width=28, height=len(self.items) + 4,
            bg=(0, 0, 0), title=" nearby "
            )

    def on_draw(self: BaseExamineMenu, consoles: Dict[str, Console]) -> None:
        self.right_panel.on_draw(consoles)

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
            self: BaseExamineMenu,
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

    def pick_item(self: BaseExamineMenu, item) -> Action:
        pass


class ExamineItemMenu(BaseExamineMenu):

    def pick_item(self: BaseExamineMenu, item) -> Action:
        self.option_list.clear()
        for component in item.components.values():
            if len(component.option) > 0:
                self.option_list.append(component.option)

        if len(self.option_list) > 0:
            state = ItemOptionsMenu(self.model, item)
            state.loop()
        else:
            return common.ActivateNearby(self.model.player.components['ACTOR'], item)


class ItemOptionsMenu(ExamineItemMenu):

    def __init__(self: ItemOptionsMenu, model: Model, item) -> None:
        super().__init__(model)
        self.right_panel = FramePanel(
            parent=self.wrapper_panel, position=("center", "right"),
            width=28, height=len(self.option_list) + 4,
            bg=(0, 0, 0), title=f" {item.noun_text} "
            )

    def on_draw(self: ItemOptionsMenu, consoles: Dict[str, Console]) -> None:
        draw_main_view(self.model, consoles)
        self.side_panel.on_draw(consoles)
        draw_log(self.model, consoles)
        self.right_panel.on_draw(consoles)

        for i, option in enumerate(self.option_list):
            sym = self.symbols[i]
            x = self.right_panel.bounds.left + 2
            y = self.right_panel.bounds.top + 2
            consoles['INTERFACE'].print(x, y + i, f"{sym}: {option}")

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
            self: ItemOptionsMenu,
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
            if index < len(self.option_list):
                option = self.option_list[index]
                return self.pick_option(option)
        return super().ev_keydown(event)

    def pick_option(self: ItemOptionsMenu, option) -> Action:
        pass

    def cmd_quit(self: ItemOptionsMenu) -> None:
        self.option_list.clear()
        raise StateBreak()


class BaseEquipmentMenu(BaseMenuOverlay):

    def __init__(self: BaseEquipmentMenu, model: Model) -> None:
        super().__init__(model)

        self.equipment = self.model.player.components['EQUIPMENT']
        self.equipment_panel = EquipmentPanel(
            parent=self.wrapper_panel,
            position=("top", "left"),
            width=(STAGE_PANEL_WIDTH // 2) - 2,
            height=STAGE_PANEL_HEIGHT,
            bg=(0, 0, 0),
            title=" equipment ",
            state=self
            )

        self.inventory = self.model.player.components['INVENTORY']
        self.inventory_panel = InventoryPanel(
            parent=self.wrapper_panel,
            position=("top", "right"),
            width=(STAGE_PANEL_WIDTH // 2) - 2,
            height=STAGE_PANEL_HEIGHT,
            bg=(0, 0, 0),
            title=" inventory ",
            state=self
            )

    def on_draw(self: BaseEquipmentMenu, consoles: Dict[str, Console]) -> None:
        self.equipment_panel.on_draw(consoles)
        self.inventory_panel.on_draw(consoles)

    def ev_keydown(self: BaseEquipmentMenu, event: tcod.event.KeyDown) -> Optional[Action]:
        char: Optional[str] = None
        try:
            char = chr(event.sym)
        except ValueError:
            pass
        return super().ev_keydown(event)

    def pick_item(self: BaseEquipmentMenu, item: Item) -> Optional[Action]:
        raise NotImplementedError()

    def cmd_quit(self: BaseEquipmentMenu) -> None:
        raise StateBreak()


class BaseInventoryMenu(BaseMenuOverlay):

    def __init__(self: BaseInventoryMenu, model: Model) -> None:
        super().__init__(model)

        self.inventory = self.model.player.components['INVENTORY']
        self.inventory_panel = InventoryPanel(
            position=("top", "right"),
            parent=self.wrapper_panel,
            width=(STAGE_PANEL_WIDTH // 2) - 2,
            height=STAGE_PANEL_HEIGHT,
            fg=(255, 255, 255),
            bg=(0, 0, 0),
            title=" inventory ",
            state=self
            )

    def on_draw(self: BaseInventoryMenu, consoles: Dict[str, Console]) -> None:
        self.inventory_panel.on_draw(consoles)

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

    def cmd_quit(self: BaseMenuOverlay) -> None:
        """Return to previous state."""
        raise StateBreak()


class UseInventory(BaseInventoryMenu):
    def pick_item(self: UseInventory, item: Item) -> Action:
        return common.ActivateItem(self.model.player.components['ACTOR'], item)


class DropInventory(BaseInventoryMenu):
    def pick_item(self: DropInventory, item: Item) -> Action:
        return common.DropItem(self.model.player.components['ACTOR'], item)


class PickLocation(AreaState[Tuple[int, int]]):
    """UI mode to prompt the user for an x,y location."""

    def __init__(
            self: PickLocation,
            model: Model,
            desc: str,
            start_xy: Tuple[int, int]
        ) -> None:
        super().__init__(model)
        self.desc = desc
        self.cursor_xy = start_xy

    def on_draw(self: PickLocation, consoles: Dict[str, Console]) -> None:
        super().on_draw(consoles)
        style = {"fg": (255, 255, 255), "bg": (0, 0, 0)}
        consoles['ROOT'].print(0, 0, self.desc, **style)
        cam_x, cam_y = self.model.current_area.get_camera_pos()
        x = self.cursor_xy[0] - cam_x
        y = self.cursor_xy[1] - cam_y
        if 0 <= x < STAGE_PANEL_WIDTH and 0 <= y < STAGE_PANEL_HEIGHT:
            consoles['ROOT'].tiles_rgb.T[["fg", "bg"]][x, y] = (255, 0, 0), (0, 0, 0)

    def cmd_move(self: PickLocation, x: int, y: int) -> None:
        x += self.cursor_xy[0]
        y += self.cursor_xy[1]
        x = min(max(0, x), self.model.current_area.width - 1)
        y = min(max(0, y), self.model.current_area.height - 1)
        if not self.model.current_area.visible[y, x]:
            self.cursor_xy = self.cursor_xy
        else:
            self.cursor_xy = x, y
            self.model.current_area.camera_pos = self.cursor_xy

    def cmd_confirm(self: PickLocation) -> Tuple[int, int]:
        return self.cursor_xy

    def cmd_quit(self: PickLocation) -> None:
        raise StateBreak()
