from __future__ import annotations  # type: ignore
from typing import Dict, Optional, TYPE_CHECKING

import sys
import os.path
import json
import datetime
import traceback

import lzma
import pickle
import pickletools
import traceback

import tcod
import numpy as np

if TYPE_CHECKING:
    from engine.paths.player import Player
    from engine.model import Model


class Storage:

    def __init__(self) -> None:
        self.save_slots: Dict[str, Optional[Model]] = {
            'slot_00': None,
            'slot_10': None,
            'slot_20': None,
            'slot_01': None,
            'slot_11': None,
            'slot_21': None,
        }

        self.save_file = "simulacra.sav.xz"
        self.save_time = datetime.datetime.now()

    def add_save(self, x: int, y: int, model: Model) -> None:
        if self.save_slots[f'slot_{x}{y}'] is None:
            self.save_slots[f'slot_{x}{y}'] = model
        else:
            raise Exception("That slot currently has save data in it!")

    def del_save(self, x: int, y: int) -> None:
        if self.save_slots[f'slot_{x}{y}'] is not None:
            self.save_slots[f'slot_{x}{y}'] = None
        
    def write_to_file(self) -> None:
        data = pickle.dumps(self.save_slots, protocol=4)
        debug = f"Raw: {len(data)} bytes, "
        data = pickletools.optimize(data)
        debug += f"Optimized: {len(data)} bytes, "
        data = lzma.compress(data)
        debug += f"Compressed: {len(data)} bytes."
        print(debug)
        print(f"Game saved on {self.save_time}")
        with open(self.save_file, "wb") as f:
            f.write(data)

    def load_from_file(self) -> None:
        try:
            with open(self.save_file, "rb") as f:
                self.save_slots = pickle.loads(lzma.decompress(f.read()))
            print(f"Loaded data from {self.save_file}.")
        except Exception:
            traceback.print_exc(file=sys.stderr)
            print("No save data found.")

    def get_character_name(self, x: int, y: int) -> str:
        if self.save_slots[f'slot_{x}{y}'] is not None:
            player: Player = self.save_slots[f'slot_{x}{y}'].player
            return player.name
        else:
            pass
        
    def get_character_background(self, x: int, y: int) -> str:
        if self.save_slots[f'slot_{x}{y}'] is not None:
            player: Player = self.save_slots[f'slot_{x}{y}'].player
            return player.background
        else:
            pass