"""
Simulacra
"""

import tcod

import config

from engine.states import MainMenuState
from engine.rendering import tileset


def main() -> None:
    """Setup the terminal and start the main game loop."""

    with tcod.context.new_terminal(
        columns=config.CONSOLE_WIDTH,
        rows=config.CONSOLE_HEIGHT,
        tileset=tileset,
        title="Simulacra",
        vsync=True
    ) as config.CONTEXT:

        while True:
            MainMenuState().loop()


if __name__ == '__main__':
    main()
