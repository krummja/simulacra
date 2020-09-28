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
from consoles import *
from engine.model import Model
from engine.area import Area
from engine.storage import Storage
from engine.procgen.test_area import *
from geometry import *

from states import State, SaveAndQuit, GameOverQuit
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

        # Character Menu
        self.character_menu = CharacterGrid(
            position=("bottom", "center"),
            width=62,
            height=20,
            vertical_offset=-4,
            bg=(50, 50, 50),
            columns=3, 
            rows=2,
        )
        self.character_menu.data_source = self.storage

        # SLOT 0
        self.character_menu.make_info_frame(
            position=("top", "left"),
            vertical_offset=0,
            horizontal_offset=0,
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=0
        )

        # SLOT 1
        self.character_menu.make_info_frame(
            position=("top", "center"),
            vertical_offset=0,
            horizontal_offset=0,
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=1
        )

        # SLOT 2
        self.character_menu.make_info_frame(
            position=("top", "right"),
            vertical_offset=0,
            horizontal_offset=0,
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=2
        )

        # SLOT 3
        self.character_menu.make_info_frame(
            position=("bottom", "left"),
            vertical_offset=0,
            horizontal_offset=0,
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=3
        )

        # SLOT 4
        self.character_menu.make_info_frame(
            position=("bottom", "center"),
            vertical_offset=0,
            horizontal_offset=0,
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=4
        )

        # SLOT 5
        self.character_menu.make_info_frame(
            position=("bottom", "right"),
            vertical_offset=0,
            horizontal_offset=0,
            margin=1,
            fg=(255, 255, 255),
            bg=(100, 0, 0),
            slot=5
        )

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(0, 0, consoles)

        load_slot = "[enter] continue, "
        create_new = "[enter] create new, "
        self.help_text = HelpText(content=[
            load_slot if self.storage.save_slots[
                self.character_menu.index_as_int
            ] is not None else create_new,
            "[⬆/⬇/⬅/➡] change selection, ", 
            "[d] delete, ",
            "[q] quit"
        ])
        
        self.character_menu.on_draw(consoles)
        self.help_text.on_draw(consoles)

    def refresh(self) -> None:
        CONSOLES['ROOT'].clear()
        self.on_draw(CONSOLES)

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        
        if key == tcod.event.K_q:
            self.cmd_quit()

        elif key == tcod.event.K_d:
            index = self.character_menu.index_as_int
            if self.storage.save_slots[index] is not None:
                self.storage.save_slots[index] = None
                self.character_menu.character_frames[index].name = "------"
                self.character_menu.character_frames[index].background = ""                
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
                index = self.character_menu.index_as_int
                self.model = self.storage.save_slots[index]
                self.start()

        elif key == tcod.event.K_ESCAPE:
            pass
        else:
            super().ev_keydown(event)

    def new_game(self) -> None:
        try:
            self.model = Model()
            self.model.current_area = test_area(self.model)
            self.storage.add_save(self.character_menu.index_as_int, self.model)
            self.start()
            # CharacterCreation(self.storage).loop()
        except SystemExit:
            raise
        
    def start(self) -> None:
        assert self.model
        try:
            print("Starting up game loop.")
            self.model.loop()
        except SaveAndQuit:
            self.storage.write_to_file()
            index = self.character_menu.index_as_int
            self.character_menu.load_slot_data(index)
            self.character_menu.refresh(index)
        except GameOverQuit:
            self.model = None
            self.storage.del_save(self.character_menu.index_as_int)
        except SystemExit:
            if self.model.player.alive:
                self.storage.write_to_file()
            else:
                print("Player has died; removing save file.")
                self.storage.del_save(self.character_menu.index_as_int)
            raise


class CharacterCreation(State[None]):

    def __init__(self, storage: Storage) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.storage = storage
    
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
            # TODO: ...abandoning character creation properties if they exit.
            self.cmd_quit()
        else:
            super().ev_keydown(event)


class BackgroundSelection(State[None]):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].clear()

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.SystemExit

        if key == tcod.event.K_q:
            self.cmd_quit()
        else:
            super().ev_keydown(event)


class PathSelection(State[None]):

    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].clear()

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key == tcod.event.K_q:
            self.cmd_quit()
        else:
            super().ev_keydown(event)
