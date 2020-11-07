from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import numpy as np

from config import *
from view import View

if TYPE_CHECKING:
    from tcod import Console


class MainMenuView(View):

    def __init__(self) -> None:
        super().__init__()
        pass

    def draw_logo(self, consoles: Dict[str, Console]) -> None:
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
                                chr(130),
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

    def draw(self, consoles: Dict[str, Console]) -> None:
        self.draw_logo(consoles)
