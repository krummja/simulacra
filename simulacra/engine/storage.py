"""ENGINE.Storage"""
from __future__ import annotations

import datetime
import lzma
import pickle
import pickletools
import sys
import traceback
from typing import TYPE_CHECKING, Dict, Optional

from config import DEBUG

if TYPE_CHECKING:
    from model import Model


class Storage:

    def __init__(self) -> None:
        self.save_slots: Dict[int, Optional[Model]] = {
            0: None, 1: None, 2: None,
            3: None, 4: None, 5: None,
            }
        self.save_file = "simulacra.sav.xz"
        self.save_time = datetime.datetime.now()
        self.debug = DEBUG

    def data_hook(self: Storage, index: int) -> Optional[Model]:
        return self.save_slots[index]

    def add_save(self: Storage, index: int, model: Model) -> None:
        if self.save_slots[index] is None:
            self.save_slots[index] = model
        else:
            raise Exception("That slot currently has save data.")

    def write_to_file(self: Storage) -> None:
        data = pickle.dumps(self.save_slots, protocol=4)
        debug = f"Raw: {len(data)} bytes ({round(len(data)/1024, 2)}kb) \n"
        data = pickletools.optimize(data)
        debug += f"Optimized: {len(data)} bytes ({round(len(data)/1024, 2)}kb) \n"
        data = lzma.compress(data)
        debug += f"Compressed: {len(data)} bytes ({round(len(data)/1024, 2)}kb)."
        with open(self.save_file, "wb") as f:
            f.write(data)
        if self.debug:
            print(debug)
            print(f"Game saved on {self.save_time}")

    def load_from_file(self: Storage) -> None:
        try:
            with open(self.save_file, "rb") as f:
                self.save_slots = pickle.loads(lzma.decompress(f.read()))
            if self.debug:
                print(f"Loaded data from {self.save_file}.")
        except Exception:
            traceback.print_exc(file=sys.stderr)
            if self.debug:
                print("No save data found.")
