from __future__ import annotations
from typing import Dict, TYPE_CHECKING

import tcod
import random
import time
import numpy as np

from config import *
from view import View
from panel import Panel
from views.elements.elem_help_text import ElemHelpText
from views.elements.elem_character_select import ElemCharacterSelect

if TYPE_CHECKING:
    from tcod import Console
    from state import State


class NoiseMachine:

    NOISE_OPTIONS = [
        ["perlin noise", tcod.NOISE_PERLIN, tcod.noise.SIMPLE]
        ]

    def __init__(self):
        self.func = 0
        self.dx = 0.0
        self.dy = 0.0
        self.octaves = 4.0
        self.zoom = 3.0
        self.hurst = tcod.NOISE_DEFAULT_HURST
        self.lacunarity = tcod.NOISE_DEFAULT_LACUNARITY
        self.noise = self.get_noise()
        self.img = tcod.image_new(CONSOLE_WIDTH * 2, CONSOLE_HEIGHT * 2)

    @property
    def algorithm(self):
        return self.NOISE_OPTIONS[self.func][1]

    @property
    def implementation(self):
        return self.NOISE_OPTIONS[self.func][2]

    def get_noise(self):
        return tcod.noise.Noise(
            2,
            self.algorithm,
            self.implementation,
            self.hurst,
            self.lacunarity,
            self.octaves,
            seed=None,
            )

    def on_enter(self):
        tcod.sys_set_fps(0)

    def on_draw(self, consoles: Dict[str, Console]):
        self.dx = time.perf_counter() * 0.25
        self.dy = time.perf_counter() * 0.25
        for y in range(2 * CONSOLE_HEIGHT):
            for x in range(2 * CONSOLE_WIDTH):
                f = [
                    self.zoom * x / (2 * CONSOLE_WIDTH) + self.dx,
                    self.zoom * y / (2 * CONSOLE_HEIGHT) + self.dy
                    ]
                value = self.noise.get_point(*f)
                c = int((value + 1.0) / 2.0 * 255)
                c = max(0, min(c, 255))
                self.img.put_pixel(x, y, (c // 2, c // 2, c))

        rectw = 24
        recth = 13
        if self.implementation == tcod.noise.SIMPLE:
            recth = 10

        consoles['INTERFACE'].draw_semigraphics(self.img)
        consoles['INTERFACE'].draw_rect(2, 2,
                                        rectw, recth,
                                        ch=0, fg=None, bg=tcod.grey,
                                        bg_blend=tcod.BKGND_MULTIPLY)

        consoles['INTERFACE'].fg[2: 2 + rectw, 2: 2 + recth] = (
            consoles['INTERFACE'].fg[2: 2 + rectw, 2: 2 + recth] * tcod.grey / 255
            )


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

        draw_logo(consoles)

        # TODO: The main menu's rendering is pinned to input - can't do this until I fix that...
        # self.background.on_draw(consoles)

        # consoles['INTERFACE'].blit(
        #     dest=consoles['ROOT'],
        #     dest_x=0,
        #     dest_y=0,
        #     width=CONSOLE_WIDTH,
        #     height=CONSOLE_HEIGHT
        #     )

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
