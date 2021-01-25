from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
import bearlibterminal as blt
from bearlibterminal import terminal

from simulacra.core.options import *
from ..manager import Manager

if TYPE_CHECKING:
    from ..game import Game


class RenderManager(Manager):
    """Manager for handling the render console."""

    def __init__(self, game: Game) -> None:
        self.game = game
        self._root_console = terminal
        self.initialize_console()

    @property
    def root_console(self):
        return self._root_console

    def clear(self) -> None:
        self._root_console.clear()

    def initialize_console(self):
        self._root_console.composition(True)
        self._root_console.open()
        window_title = "Simulacra"
        size = f"size={CONSOLE_WIDTH}x{CONSOLE_HEIGHT}"
        title = f"title={window_title}"
        cellsize = f"cellsize={20//2}x{20}"
        window = "window: " + ", " + size + "," + title + "," + cellsize

        self._root_console.set(window)
        self._root_console.set("font: default")
        self.initialize_tiles(TILE_DATA[DEFAULT_TILESET])
        self._root_console.refresh()

    def initialize_tiles(self, tiledata):
        datastring = ""
        datastring += tiledata['codepoint'] + ": "
        datastring += tiledata['path'] + ", "
        datastring += "codepage=" + tiledata['codepage'] + ", "
        datastring += "size=" + tiledata['size'] + ", "
        # datastring += 'resize=' + tiledata['resize'] + ", "
        # datastring += 'resize-filter=' + tiledata['resize-filter'] + ", "
        datastring += "align=" + tiledata['align'] + ", "
        datastring += "spacing=" + tiledata['spacing']
        self._root_console.set(datastring)


TILE_DATA = {
    'Simulacra': {
        'address': 0xE000,
        'codepoint': 'U+E000',
        'path': './simulacra/assets/Simulacra_20x20_BLT.png',
        'codepage': '1250',
        'size': '20x20',
        'resize': '40x40',
        'resize-filter': 'none',
        'align': 'center',
        'spacing': '4x4'
        },
    'ASCII': {
        'address': 0xE500,
        'codepoint': 'U+E500',
        'path': './simulacra/assets/',
        'codepage': '1250',
        'size': '20x20',
        'align': 'center',
        'spacing': '2x2'
        }
    }

def tilemap(tileset=None):
    tiles = {}

    if tileset is None:
        tileset = DEFAULT_TILESET

    if tileset == "Simulacra":
        tiles = {
            "bricks": (0xE000+0, 0xE000+1, 0xE000+2),
            }

    elif tileset == "ASCII":
        tiles = {}

    tile_data = TILE_DATA[tileset]
    return tiles, tile_data
