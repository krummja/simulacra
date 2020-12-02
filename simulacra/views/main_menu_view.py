from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
import random
import time
import numpy as np

from data.interface_elements import delete

from config import *
from view import View
from panel import Panel
from views.elements.elem_help_text import ElemHelpText
from views.elements.elem_character_select import ElemCharacterSelect
from noise_machine import NoiseMachine

from interface_element import InterfaceElement
# from managers.manager_service import ManagerService
# from factories.factory_service import FactoryService

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
        
        load = "[enter] continue, "
        new = "[enter] create new, "
        help_text = ElemHelpText(content=[
            load if self.state.storage.save_slots[
                    self.character_select.index_as_int
                    ] is not None else new,
            "[⬆/⬇/⬅/➡] change selection, ",
            "[d] delete, ",
            "[q] quit"
            ])
        help_text.draw(consoles)