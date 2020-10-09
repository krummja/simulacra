from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

from config import *
from interface.panel import Panel
from interface.frame_panel import FramePanel

if TYPE_CHECKING:
    from engine.model import Model
    from engine.components.inventory import Inventory
    from states.in_game import AreaState


class EquipmentPanel(Panel):

    def __init__(
            self: EquipmentPanel,
            position: Optional[Tuple[str, str]] = None,
            parent: Panel = None,
            width: int = CONSOLE_WIDTH,
            height: int = 0,
            margin: int = 0,
            vertical_offset: int = 0,
            horizontal_offset: int = 0,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (0, 0, 0),
            title: str="",
            state: AreaState=None
        ) -> None:
        super().__init__(
            position=position,
            parent=parent,
            width=width,
            height=height,
            margin=margin,
            vertical_offset=vertical_offset,
            horizontal_offset=horizontal_offset,
            fg=fg,
            bg=bg
            )
        self.title = title
        self.state = state

    @property
    def model(self: EquipmentPanel) -> Model:
        return self.state.model

    @property
    def inventory(self: EquipmentPanel) -> Inventory:
        return self.model.player.components['INVENTORY']

    @property
    def equipment(self: EquipmentPanel):
        return self.model.player.components['EQUIPMENT']

    def on_draw(self: EquipmentPanel, consoles: Dict[str, Console]) -> None:
        consoles['INTERFACE'].draw_frame(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            fg=self.fg,
            bg=self.bg
            )

        consoles['INTERFACE'].print(
            x=self.x+2,
            y=self.y,
            string=self.title
            )

        consoles['INTERFACE'].blit(
            dest=consoles['ROOT'],
            dest_x=self.x,
            dest_y=self.y,
            src_x=self.x,
            src_y=self.y,
            width=self.width,
            height=self.height,
            )
