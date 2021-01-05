"""
Simulacra
"""

import tcod

import config

from engine.states import MainMenuState
from engine.tiles.tilemap import tileset

from engine.apparata.parser.generator import Generator

from engine.geometry.circ import Circ
from engine.geometry.point import Point


def main() -> None:
    """Setup the terminal and start the main game loop."""

    # circle = Circ.from_edges(top=0, left=0, radius=20)
    # circle2 = Circ.centered_at(radius=21, center=Point(60, 20))

    # generator = Generator()
    # path = "/home/krummja/Workspace/Python/Simulacra/simulacra/"
    # generator.generate_from_file(path + 'engine/apparata/grammars/test.txt')

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
