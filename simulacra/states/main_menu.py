from __future__ import annotations  # type: ignore
from typing import Dict, Optional, TYPE_CHECKING

import sys
import os.path

import lzma
import pickle
import pickletools
import traceback

import tcod
import numpy as np

from constants import *
from engine.model import Model
from engine.area import Area
from engine.storage import Storage
from engine.procgen.dungeon import *
from geometry import *

from states import State
from states.character_creation import CharacterCreation
from interface.panel import Panel
from interface.modal import Modal
from interface.info_frame import InfoFrame
from interface.help_text import HelpText
from interface.logo import draw_logo

if TYPE_CHECKING:
    import tcod.console as Console


class MainMenu(State[None]):

    save_x: int = 0
    save_y: int = 0

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.storage = Storage()
        self.storage.load_from_file()
            
    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(0, 0, consoles)

        character_panel = Panel(position=("bottom", "center"),
                                width=64,
                                height=20,
                                vertical_offset=-4,
                                bg=(50, 50, 50))

        slot_inactive = (50, 0, 0)
        slot_active = (100, 0, 50)
        slot_00_bg = slot_active if self.save_x == 0 and \
                                    self.save_y == 0 else slot_inactive
        slot_10_bg = slot_active if self.save_x == 1 and \
                                    self.save_y == 0 else slot_inactive
        slot_20_bg = slot_active if self.save_x == 2 and \
                                    self.save_y == 0 else slot_inactive
        slot_01_bg = slot_active if self.save_x == 0 and \
                                    self.save_y == 1 else slot_inactive
        slot_11_bg = slot_active if self.save_x == 1 and \
                                    self.save_y == 1 else slot_inactive
        slot_21_bg = slot_active if self.save_x == 2 and \
                                    self.save_y == 1 else slot_inactive

        # TODO: This needs to be significantly cleaned up - what is the best way to access this kind of info?
        slot00 = InfoFrame(position=("top", "left"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=1,
                      bg=slot_00_bg,
                      name=self.storage.get_character_name(0, 0) if self.storage.save_slots['slot_00'] is not None else 'Empty',
                      level="1",
                      background=self.storage.get_character_background(0, 0) if self.storage.save_slots['slot_00'] is not None else 'Empty',
                      path="",
                      location="").on_draw(consoles)

        slot10 = Panel(position=("top", "center"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      bg=slot_10_bg).on_draw(consoles)

        slot20 = Panel(position=("top", "right"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=-1,
                      bg=slot_20_bg).on_draw(consoles)

        slot01 = Panel(position=("bottom", "left"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=1,
                      bg=slot_01_bg).on_draw(consoles)

        slot11 = Panel(position=("bottom", "center"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      bg=slot_11_bg).on_draw(consoles)

        slot21 = Panel(position=("bottom", "right"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=-1,
                      bg=slot_21_bg).on_draw(consoles)

        load_slot = "[enter] continue, "
        create_new = "[enter] create new, "
        HelpText(content=[
            create_new if self.storage.save_slots[
                f'slot_{self.save_x}{self.save_y}'
            ] == 'Empty' else load_slot,
            "[⬆/⬇/⬅/➡] change selection, ", 
            "[d] delete, ",
            "[q] quit"
        ]).on_draw(consoles)

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        
        if key == tcod.event.K_c and self.model:
            self.start()
        elif key == tcod.event.K_q:
            self.cmd_quit()
        elif key == tcod.event.K_d:
            self.storage.del_save(self.save_x, self.save_y)
            print(f"Deleted save file data at slot_{self.save_x}{self.save_y}")
            self.storage.write_to_file()
        elif event.sym in self.MOVE_KEYS:
            offset_x = self.MOVE_KEYS[event.sym][0]
            offset_y = self.MOVE_KEYS[event.sym][1]

            self.save_x += offset_x
            self.save_y += offset_y

            self.save_x = np.clip(self.save_x, 0, 2)
            self.save_y = np.clip(self.save_y, 0, 1)

        elif key == tcod.event.K_RETURN:
            if self.storage.save_slots[f'slot_{self.save_x}{self.save_y}'] is None:
                self.new_game()
            else:
                self.model = self.storage.save_slots[f'slot_{self.save_x}{self.save_y}']
                self.start()
        else:
            super().ev_keydown(event)

    def new_game(self) -> None:
        # try:
        #     CharacterCreation().loop()
        # except SystemExit:
        #     raise
        self.model = Model()
        self.model.current_area = generate(self.model, 256, 256)
        self.storage.add_save(self.save_x, self.save_y, self.model)
        self.start()
        
    def start(self) -> None:
        assert self.model
        try:
            print("Starting up game loop.")
            self.model.loop()
        except SystemExit:
            self.storage.write_to_file()
            raise