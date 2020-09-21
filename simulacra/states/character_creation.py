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
from interface.panel import Panel
from interface.modal import Modal
from interface.help_text import HelpText
from interface.logo import draw_logo

if TYPE_CHECKING:
    import tcod.console as Console

SAVE_FILE_NAME = "save.sav.xz"


class CharacterCreation(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
    
    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].clear()
        consoles['ROOT'].print(20, 20, "Character Creation Test")

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym

        if key == tcod.event.K_c and self.model:
            self.start()
        elif key == tcod.event.K_q:
            self.cmd_quit()
        else:
            super().ev_keydown(event)

    def start(self) -> None:
        pass