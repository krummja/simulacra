from __future__ import annotations

from config import *
from states.main_menu_state import MainMenuState


def main() -> None:
    with tcod.context.new_terminal(
            columns=CONSOLE_WIDTH,
            rows=CONSOLE_HEIGHT,
            tileset=TILESET,
            title="Simulacra",
            vsync=True
        ) as context:
        while True:
            MainMenuState().loop(context)


if __name__ == '__main__':
    main()
