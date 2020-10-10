from __future__ import annotations
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

import numpy as np

from config import *

from interface.panel import Panel
from interface.frame_panel import FramePanel

if TYPE_CHECKING:
    from storage import Storage
    from tcod.console import Console
    from engine.model import Model


class CharacterMenu(Panel):

    _data_source: Storage = None

    rows: int = 3
    cols: int = 2
    menu_cells = np.arange(rows * cols).reshape(rows, cols)

    x_index: int = 0
    y_index: int = 0

    focused = (255, 0, 255)
    unfocused = (255, 255, 255)

    wrapper = Panel(
        position=("bottom", "center"),
        width=(CONSOLE_WIDTH // 6) * 4, height=12,
        margin=5
        )

    column1 = Panel(
        parent=wrapper, position=("center", "left"),
        width=wrapper.width//2, height=wrapper.height,
        )

    column2 = Panel(
        parent=wrapper, position=("center", "right"),
        width=wrapper.width//2, height=wrapper.height,
        )

    slot_0 = FramePanel(
        parent=column1, position=("top", "center"),
        width=column1.width - 2, height=4,
        )

    slot_1 = FramePanel(
        parent=column1, position=("center", "center"),
        width=column1.width - 2, height=4,
        )

    slot_2 = FramePanel(
        parent=column1, position=("bottom", "center"),
        width=column1.width - 2, height=4,
        )

    slot_3 = FramePanel(
        parent=column2, position=("top", "center"),
        width=column2.width - 2, height=4,
        )

    slot_4 = FramePanel(
        parent=column2, position=("center", "center"),
        width=column2.width - 2, height=4,
        )

    slot_5 = FramePanel(
        parent=column2, position=("bottom", "center"),
        width=column2.width - 2, height=4,
        )

    def on_draw(self: CharacterMenu, consoles: Dict[str, Console]) -> None:
        slot_0_data = self.data_source.save_slots[0]
        slot_1_data = self.data_source.save_slots[2]
        slot_2_data = self.data_source.save_slots[4]
        slot_3_data = self.data_source.save_slots[1]
        slot_4_data = self.data_source.save_slots[3]
        slot_5_data = self.data_source.save_slots[5]

        self.slot_0.fg = self.focused if self.current_index == (0, 0) else self.unfocused
        self.slot_1.fg = self.focused if self.current_index == (1, 0) else self.unfocused
        self.slot_2.fg = self.focused if self.current_index == (2, 0) else self.unfocused
        self.slot_3.fg = self.focused if self.current_index == (0, 1) else self.unfocused
        self.slot_4.fg = self.focused if self.current_index == (1, 1) else self.unfocused
        self.slot_5.fg = self.focused if self.current_index == (2, 1) else self.unfocused

        self.slot_0.on_draw(consoles)
        self.slot_1.on_draw(consoles)
        self.slot_2.on_draw(consoles)
        self.slot_3.on_draw(consoles)
        self.slot_4.on_draw(consoles)
        self.slot_5.on_draw(consoles)

        consoles['ROOT'].print(
            self.slot_0.x+1, self.slot_0.y+1,
            slot_0_data.player.noun_text if slot_0_data is not None else "<empty>")
        consoles['ROOT'].print(
            self.slot_0.x+1, self.slot_0.y+2,
            slot_0_data.player.background_name if slot_0_data is not None else "")
        consoles['ROOT'].print(
            self.slot_0.x+26, self.slot_0.y+1,
            f"lv. {slot_0_data.player.level_as_str}" if slot_0_data is not None else "")

        consoles['ROOT'].print(
            self.slot_1.x+1, self.slot_1.y+1,
            slot_1_data.player.noun_text if slot_1_data is not None else "<empty>")
        consoles['ROOT'].print(
            self.slot_1.x+1, self.slot_1.y+2,
            slot_1_data.player.background_name if slot_1_data is not None else "")
        consoles['ROOT'].print(
            self.slot_1.x+26, self.slot_1.y+1,
            f"lv. {slot_1_data.player.level_as_str}" if slot_1_data is not None else "")

        consoles['ROOT'].print(
            self.slot_2.x+1, self.slot_2.y+1,
            slot_2_data.player.noun_text if slot_2_data is not None else "<empty>")
        consoles['ROOT'].print(
            self.slot_2.x+1, self.slot_2.y+2,
            slot_2_data.player.background_name if slot_2_data is not None else "")
        consoles['ROOT'].print(
            self.slot_2.x+26, self.slot_2.y+1,
            f"lv. {slot_2_data.player.level_as_str}" if slot_2_data is not None else "")

        consoles['ROOT'].print(
            self.slot_3.x+1, self.slot_3.y+1,
            slot_3_data.player.noun_text if slot_3_data is not None else "<empty>")
        consoles['ROOT'].print(
            self.slot_3.x+1, self.slot_3.y+2,
            slot_3_data.player.background_name if slot_3_data is not None else "")
        consoles['ROOT'].print(
            self.slot_3.x+26, self.slot_3.y+1,
            f"lv. {slot_3_data.player.level_as_str}" if slot_3_data is not None else "")

        consoles['ROOT'].print(
            self.slot_4.x+1, self.slot_4.y+1,
            slot_4_data.player.noun_text if slot_4_data is not None else "<empty>")
        consoles['ROOT'].print(
            self.slot_4.x+1, self.slot_4.y+2,
            slot_4_data.player.background_name if slot_4_data is not None else "")
        consoles['ROOT'].print(
            self.slot_4.x+26, self.slot_4.y+1,
            f"lv. {slot_4_data.player.level_as_str}" if slot_4_data is not None else "")

        consoles['ROOT'].print(
            self.slot_5.x+1, self.slot_5.y+1,
            slot_5_data.player.noun_text if slot_5_data is not None else "<empty>")
        consoles['ROOT'].print(
            self.slot_5.x+1, self.slot_5.y+2,
            slot_5_data.player.background_name if slot_5_data is not None else "")
        consoles['ROOT'].print(
            self.slot_5.x+26, self.slot_5.y+1,
            f"lv. {slot_5_data.player.level_as_str}" if slot_5_data is not None else "")

    @property
    def data_source(self: CharacterMenu):
        return self._data_source

    @data_source.setter
    def data_source(self: CharacterMenu, value):
        self._data_source = value

    @property
    def current_index(self: CharacterMenu) -> Tuple[int, int]:
        return self.y_index, self.x_index

    @current_index.setter
    def current_index(self: CharacterMenu, value: Tuple[int, int]) -> None:
        self.x_index += value[0]
        self.x_index = max(0, min(self.x_index, self.cols-1))
        self.y_index += value[1]
        self.y_index = max(0, min(self.y_index, self.rows-1))

    @property
    def index_as_int(self: CharacterMenu) -> int:
        return self.menu_cells[self.current_index]

    @property
    def data_at_index(self) -> Optional[Model]:
        if self.data_source:
            return self._data_source.data_hook(self.index_as_int)
        else:
            raise Exception("No data source assigned to this menu!")
