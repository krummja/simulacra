"""
Simulacra
"""

import tcod

import config

from engine.states import MainMenuState
from engine.rendering import tileset

from engine.apparata.parser.generator import Generator

def main() -> None:
    """Setup the terminal and start the main game loop."""

    generator = Generator()
    PATH = "/home/krummja/Workspace/Python/Simulacra/simulacra/"
    generator.generate_from_file(PATH + 'engine/apparata/grammars/test.txt')

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
