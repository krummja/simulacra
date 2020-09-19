#!/usr/lib/python3.8

from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import tcod

from states.main_menu import MainMenu

import globals as g
from consoles import CONSOLES, CONSOLE_WIDTH, CONSOLE_HEIGHT, TILESET
from constants import *


def main() -> None:
    with tcod.context.new_terminal(
            columns=CONSOLE_WIDTH,
            rows=CONSOLE_HEIGHT,
            tileset=TILESET,
            title="Simulacra",
            vsync=True
        ) as g.context:
        
        while True:
            MainMenu().loop()


if __name__ == '__main__':
    main()