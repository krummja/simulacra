from __future__ import annotations  # type: ignore
from typing import Dict, Optional, TYPE_CHECKING

import tcod
import numpy as np

from simulacra.constants import *
from simulacra.engine.model import Model
from simulacra.engine.area import Area

from simulacra.states import State

if TYPE_CHECKING:
    import tcod.console as Console


class MainMenu(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.continue_message = "No characters! Please create a new one."

    def on_draw(self, consoles: Dict[str, Console]) -> None:

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
                                chr(127),
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

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        
        if key == tcod.event.K_c and self.model:
            self.start()
        elif key == tcod.event.K_n:
            self.new_game()
        elif key == tcod.event.K_q:
            self.cmd_quit()
        else:
            super().ev_keydown(event)

    def new_game(self) -> None:
        self.model = Model()
        self.model.current_area = Area(self.model, STAGE_WIDTH, STAGE_HEIGHT)
        self.start()
        
    def start(self) -> None:
        assert self.model
        try:
            self.model.loop()
        except SystemExit:
            raise

    def save(self) -> None:
        pass

    def remove_save(self) -> None:
        pass