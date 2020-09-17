from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import tcod
from simulacra.constants import *
context: tcod.context.Context

if TYPE_CHECKING:
    import tcod.console as Console
    import tcod.context as Context


CONSOLES = {
    'BACKGROUND': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        order="F"
    ),
    'FOREGROUND': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        order="F"
    ),
    'EFFECTS': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        order="F"
    ),
    'INTERFACE': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        order="F"
    ),
    'ROOT': tcod.Console(
        CONSOLE_WIDTH,
        CONSOLE_HEIGHT,
        order="F"
    ),
}