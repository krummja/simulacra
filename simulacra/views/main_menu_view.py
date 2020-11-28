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
from managers.manager_service import ManagerService
from factories.factory_service import FactoryService

from panel import Panel

if TYPE_CHECKING:
    from tcod import Console
    from state import State


def draw_logo(consoles: Dict[str, Console]) -> None:
    logo = np.array([
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        "!!                                                                              !!",
        "!  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  !",
        "! @@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "! @  ########  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "! @ ########## @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "! @ ##      ##   @@@@@                   @@@@@   @@              @@@@@@@   @@@@@ !",
        "! @ ##  @@ #####  @@@  ###### #### ##### @@@@  # @  ############  @@@@@  # @@@@@ !",
        "! @ ###  @  #####  @@@  #####  ###  ###  @@@  ##   ##### ######## @@@@  ## @@@@@ !",
        "! @  ###  @ ## ###  @  ### ##   ##  ##  @@@  ###  ###  # ##    ## @@@  ### @@@@@ !",
        "! @@  ###   ## ####   #### ## @ ##  ## @@@  #### ###     ##   ### @@  #### @@@@@ !",
        "! @@@  ###  ## ##### ##### ## @ ##  ## @@  ##### ##  @@@ ## ####  @  ##### @@@@@ !",
        "! @@@@  ### ## ## ##### ## ##   ###### @  ### ## ## @@@@ ######  @  ### ## @@@@@ !",
        "! @@@@@  ## ## ##  ###  ## ### #### ##   ###  ## ## @@@@ ##  ###   ###  ## @@@@@ !",
        "! @     ### ## ##   #   ##  ######  ##  ###   ## ##  @@  ##   ##  ###   ##   @@@ !",
        "! @ ######  ##### @    ###  ######  ##  ############ @  ### @ ##  ########## @@@ !",
        "! @ #####   ##### @@@ #####   # ## ####  ######## ##   #### @  ##  ########    @ !",
        "! @ #     @ ##    @@@       @     ######        ######        ####          ## @ !",
        "! @   @@@@@ ####  @@@@@@@@@@@@@@@    ######    ##########    #########  #####  @ !",
        "! @@@@@@@@@ ###  @@@@@@@@@@@@@@@@@@@   ###########   ###########  ##########  @@ !",
        "! @@@@@@@@@ ##  @@@@@@@@@@@@@@@@@@@@@@    ######        ######       ####    @@@ !",
        "! @@@@@@@@@ #  @@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@@        @@@@@      @@@@@@ !",
        "! @@@@@@@@@   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ !",
        "!  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  !",
        "!!                                                                              !!",
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",
        ])

    consoles['ROOT'].clear()
    logo = np.array([list(line) for line in logo])
    height = logo.shape[0]

    vertical_offset: int = 4

    row_index = 0
    for line in logo:
        width = len(line)
        col_index = 0
        if row_index <= height:
            for char in line:
                if col_index <= width:
                    if char == "#":
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            chr(42),
                            fg=(200, 100, 155)
                            )

                    elif char == "@":
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            chr(42),
                            fg=(100, 0, 0)
                            )

                    elif char == "!":
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            chr(35),
                            fg=(200, 155, 155)
                            )

                    else:
                        consoles['ROOT'].print(
                            ((CONSOLE_WIDTH - width) // 2) + col_index,
                            vertical_offset + row_index,
                            " "
                            )

                    col_index += 1
            row_index += 1


class MainMenuView(View):

    index = 0

    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state
        self.character_select = ElemCharacterSelect()
        self.character_select.data_source = state.storage
        # self.background = NoiseMachine()

    def draw(self, consoles: Dict[str, Console]) -> None:
        # self.background.on_draw(consoles)
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
        
        if self.state.delete:
            Panel(**delete).on_draw(consoles)
        # InterfaceElement(10, 10, 50, 20, "Text").draw(consoles)
        # self.factory_service.interface_factory.build('test_element').draw(consoles)