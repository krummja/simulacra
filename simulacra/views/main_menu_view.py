from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
import random
import time
import numpy as np

from message import ColorFormatter

from data.interface_elements import delete

from hues import set_color, RESET
from config import *
from view import View
from panel import Panel
from views.elements.help_text_element import HelpTextElement
from views.elements.elem_character_select import ElemCharacterSelect
from noise_machine import NoiseMachine

from panel import Panel
from rendering import draw_logo

if TYPE_CHECKING:
    from tcod import Console
    from state import State


class MainMenuView(View):

    index = 0

    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state
        self.character_select = ElemCharacterSelect()
        self.character_select.data_source = state.storage

    def draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(consoles)
        
        self.character_select.draw(consoles)
        
        YELLOW = set_color(fg=(255, 255, 0))
        RED = set_color(fg=(100, 255, 0))
        
        load = f"[ENTER]:continue, ".upper()
        new = "[ENTER]:create new, ".upper()
        load_new_option = load if self.state.storage.save_slots[
            self.character_select.index_as_int
        ] is not None else new
        selection_option = "[⬆/⬇/⬅/➡]:change selection, ".upper()
        delete_option = "[D]:delete, ".upper()
        quit_option = "[Q]:quit ".upper()
        
        help_text = HelpTextElement(help_options=[load_new_option, 
                                                  selection_option, 
                                                  delete_option, 
                                                  quit_option],
                                    hue=(255, 0, 0))
        help_text.draw(consoles)
        
        