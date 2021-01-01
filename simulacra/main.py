"""
Simulacra
"""

import tcod

import config

from engine.states import MainMenuState
from engine.rendering import tileset

from engine.apparata.parser.generator import Generator
from engine.apparata.graph import Graph, GraphQuery

def main() -> None:
    """Setup the terminal and start the main game loop."""

    generator = Generator()
    path = "/home/krummja/Workspace/Python/Simulacra/simulacra/"
    generator.generate_from_file(path + 'engine/apparata/grammars/test.txt')

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
