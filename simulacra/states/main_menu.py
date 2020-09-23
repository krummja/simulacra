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
from interface.panel import Panel
from interface.modal import Modal
from interface.info_frame import InfoFrame
from interface.help_text import HelpText
from interface.logo import draw_logo
from interface.character_grid import CharacterGrid

if TYPE_CHECKING:
    import tcod.console as Console


class MainMenu(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.storage = Storage()
        self.storage.load_from_file()

        self.character_menu = CharacterGrid(
            position=("bottom", "center"),
            width=64,
            height=20,
            vertical_offset=-4,
            bg=(50, 50, 50),
            columns=3, 
            rows=2,
        )
        self.character_menu.data_source = self.storage
        self.character_menu.make_info_frame(
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=0
        )

        load_slot = "[enter] continue, "
        create_new = "[enter] create new, "
        self.help_text = HelpText(content=[
            # TODO: Fix load/create
            "[⬆/⬇/⬅/➡] change selection, ", 
            "[d] delete, ",
            "[q] quit"
        ])

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(0, 0, consoles)

        self.character_menu.on_draw(consoles)
        self.help_text.on_draw(consoles)

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        
        if key == tcod.event.K_q:
            self.cmd_quit()

        elif key == tcod.event.K_d:
            # TODO: FIX ME
            # self.storage.del_save(self.character_menu.current_index)
            # print(f"Deleted save file data at slot_{self.character_menu.current_index}")
            self.storage.write_to_file()

        elif event.sym in self.MOVE_KEYS:
            self.character_menu.current_index = (
                self.MOVE_KEYS[event.sym][0],
                self.MOVE_KEYS[event.sym][1]
            )

        elif key == tcod.event.K_RETURN:
            menu_data = self.character_menu.data_at_index
            
            if menu_data is None:
                self.new_game()
            else:
                index = self.character_menu.current_index
                self.model = self.storage.save_slots[index]
                self.start()

        elif key == tcod.event.K_ESCAPE:
            pass
        else:
            super().ev_keydown(event)

    def new_game(self) -> None:
        try:
            CharacterCreation().loop()
        except SystemExit:
            raise
        # self.model = Model()
        # self.model.current_area = generate(self.model, 256, 256)
        # self.storage.add_save(self.save_x, self.save_y, self.model)
        # self.start()
        
    def start(self) -> None:
        assert self.model
        try:
            print("Starting up game loop.")
            self.model.loop()
        except SystemExit:
            self.storage.write_to_file()
            raise

class CharacterCreation(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
    
    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].clear()

        HelpText(content=[
            "[esc] return to main, ",
            "[enter] begin, ",
            "[⬆/⬇/⬅/➡] change selection, ", 
            "[q] quit"
        ]).on_draw(consoles)

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key == tcod.event.K_RETURN and self.model:
            self.start()

        elif key == tcod.event.K_q:
            # TODO: Raise a confirmation modal, as the player will likely be
            # TODO: abandoning character creation properties if they exit.
            self.cmd_quit()
        else:
            super().ev_keydown(event)

    def start(self) -> None:
        pass