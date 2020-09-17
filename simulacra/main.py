from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from simulacra.consoles import *
from simulacra.constants import *


def main() -> None:
    with tcod.context.new_terminal(
            columns=CONSOLE_WIDTH,
            rows=CONSOLE_HEIGHT,
            tileset=TILESET,
            title="Simulacra",
            vsync=True
        ) as context:
        
        while True:
            pass


if __name__ == '__main__':
    main()