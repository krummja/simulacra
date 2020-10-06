from __future__ import annotations

import tcod.context

import config
from states.main_menu import MainMenu


def main() -> None:
    with tcod.context.new_terminal(
            columns=config.CONSOLE_WIDTH,
            rows=config.CONSOLE_HEIGHT,
            tileset=config.TILESET,
            title="Simulacra",
            vsync=True
        ) as config.CONTEXT:

        while True:
            MainMenu().loop()


if __name__ == '__main__':
    main()
