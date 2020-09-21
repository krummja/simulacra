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
from engine.procgen.dungeon import *
from geometry import *

from states import State
from states.character_creation import CharacterCreation
from interface.panel import Panel
from interface.modal import Modal
from interface.help_text import HelpText
from interface.logo import draw_logo

if TYPE_CHECKING:
    import tcod.console as Console


class MainMenu(State[None]):

    save_x: int = 0
    save_y: int = 0

    SAVE_SLOTS = {
        'slot_00': None,
        'slot_10': None,
        'slot_20': None,
        'slot_01': None,
        'slot_11': None,
        'slot_21': None,
    }

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.continue_message = "No characters! Please create a new one."
        self.SAVE_FILE = f"slot_{self.save_x}{self.save_y}.sav.xz"

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(0, 0, consoles)

        character_panel = Panel(position=("bottom", "center"),
                                width=64,
                                height=20,
                                vertical_offset=-4,
                                bg=(50, 50, 50))

        slot_inactive = (50, 0, 0)
        slot_active = (100, 0, 50)
        slot_00_bg = slot_active if self.save_x == 0 and self.save_y == 0 else slot_inactive
        slot_10_bg = slot_active if self.save_x == 1 and self.save_y == 0 else slot_inactive
        slot_20_bg = slot_active if self.save_x == 2 and self.save_y == 0 else slot_inactive
        slot_01_bg = slot_active if self.save_x == 0 and self.save_y == 1 else slot_inactive
        slot_11_bg = slot_active if self.save_x == 1 and self.save_y == 1 else slot_inactive
        slot_21_bg = slot_active if self.save_x == 2 and self.save_y == 1 else slot_inactive

        slot00 = Panel(position=("top", "left"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=1,
                      bg=slot_00_bg).on_draw(consoles)

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
            create_new if self.SAVE_SLOTS[f'slot_{self.save_x}{self.save_y}'] is None else load_slot, 
            "[⬆/⬇/⬅/➡] change selection, ", 
            "[d] delete, ",
            "[q] quit"
        ]).on_draw(consoles)

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        
        if key == tcod.event.K_c and self.model:
            self.start()
        elif key == tcod.event.K_n:
            self.new_game()
        elif key == tcod.event.K_q:
            self.cmd_quit()
        elif event.sym in self.MOVE_KEYS:
            offset_x = self.MOVE_KEYS[event.sym][0]
            offset_y = self.MOVE_KEYS[event.sym][1]

            self.save_x += offset_x
            self.save_y += offset_y

            self.save_x = np.clip(self.save_x, 0, 2)
            self.save_y = np.clip(self.save_y, 0, 1)

            self.SAVE_FILE = f"slot_{self.save_x}{self.save_y}.sav.xz"
        elif key == tcod.event.K_RETURN:
            if self.SAVE_SLOTS[f'slot_{self.save_x}{self.save_y}'] is None:
                self.new_game()
            else:
                self.load()
        else:
            super().ev_keydown(event)

    def new_game(self) -> None:
        # try:
        #     CharacterCreation().loop()
        # except SystemExit:
        #     raise
        self.model = Model()
        self.model.current_area = generate(self.model, 256, 256)
        self.start()
        
    def start(self) -> None:
        assert self.model
        try:
            print("Starting up game loop.")
            self.model.loop()
        except SystemExit:
            self.save()
            raise

    def save(self) -> None:
        data = pickle.dumps(self.model, protocol=4)
        debug = f"Raw: {len(data)} bytes, "
        data = pickletools.optimize(data)
        debug += f"Optimized: {len(data)} bytes, "
        data = lzma.compress(data)
        debug += f"Compressed: {len(data)} bytes."
        print(debug)
        print("Game saved.")
        with open(self.SAVE_FILE, "wb") as f:
            f.write(data)

        self.SAVE_SLOTS[f'{self.save_x}{self.save_y}'] = self.model

    def load(self) -> None:
        try:
            with open(self.SAVE_FILE, "rb") as f:
                self.model = pickle.loads(lzma.decompress(f.read()))
            print(f"Loaded data from {self.SAVE_FILE}.")
        except Exception:
            traceback.print_exc(file=sys.stderr)
            print("Error loading save.")

    def remove_save(self) -> None:
        if os.path.exists(self.SAVE_FILE):
            os.remove(self.SAVE_FILE)

