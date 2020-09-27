from __future__ import annotations  # type: ignore
from typing import Any, Dict, Optional, Tuple, TYPE_CHECKING

import numpy as np
from consoles import *
from interface.grid_menu import GridMenu
from interface.info_frame import InfoFrame
from interface.panel import Panel

if TYPE_CHECKING:
    import tcod.console as Console
    from engine.model import Model


class CharacterGrid(GridMenu):

    def __init__(
            self,
            position: Optional[Tuple[str, str]]=None,
            parent: Optional[Panel]=None,
            width: int=0,
            height: int=0,
            margin: int=0,
            vertical_offset: int=0,
            horizontal_offset: int=0,
            fg: Tuple[int, int, int]=(255, 255, 255),
            bg: Tuple[int, int, int]=(0, 0, 0),
            columns: int=0, 
            rows: int=0,
        ) -> None:
        """The entries in the grid menu are stored as an integer array, which
        allows for easy navigation by hooking into the movement system.
        """
        super().__init__(
            position=position,
            parent=parent,
            width=width,
            height=height,
            margin=margin,
            vertical_offset=vertical_offset,
            horizontal_offset=horizontal_offset,
            fg=fg,
            bg=bg,
            columns=columns,
            rows=rows,
        )
        self.character_frames = []

    def make_info_frame(
            self,
            position,
            vertical_offset,
            horizontal_offset,
            margin,
            fg,
            bg,
            slot,
        ) -> None:
        frame_width = self.width // self.columns - (2 * margin)
        frame_height = self.height // self.rows - (2 * margin)

        character_name, character_background = self.load_slot_data(slot)

        new_frame = InfoFrame(
                position=position,
                parent=self,
                width=frame_width,
                height=frame_height,
                margin=margin,
                vertical_offset=vertical_offset,
                horizontal_offset=horizontal_offset,
                fg=fg,
                bg=bg,
                name=character_name,
                background=character_background
            )
        new_frame.id = slot
        self.character_frames.append(new_frame)

    def load_slot_data(self, slot: int) -> Model:
        slot_data: Model = self.data_source.save_slots[slot]

        if slot_data is not None:
            print("Found slot data.")
            character_name = self.data_source.get_character_name(slot)
            character_background = slot_data.player.background
        else:
            character_name = "------"
            character_background = "---"

        return character_name, character_background

    def refresh(self, slot: int) -> None:
        CONSOLES['ROOT'].clear()
        frame = self.character_frames[slot]
        frame.name = self.data_source.get_character_name(slot)

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        for frame in self.character_frames:
            if frame.id == self.index_as_int:
                frame.bg = (200, 100, 155)
            else:
                frame.bg = (50, 0, 0)
            frame.on_draw(consoles)