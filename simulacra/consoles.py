from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import tcod
from constants import *

if TYPE_CHECKING:
    import tcod.console as Console


CONSOLES = {
    'BACKGROUND': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        # order="F"
    ),
    'FOREGROUND': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        # order="F"
    ),
    'EFFECTS': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        # order="F"
    ),
    'INTERFACE': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        # order="F"
    ),
    'ROOT': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        # order="F"
    ),
}