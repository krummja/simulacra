from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from bearlibterminal import terminal
from simulacra.core.options import *

from ..manager import Manager
from .sprite_registry import SpriteRegistry

if TYPE_CHECKING:
    from ..game import Game


@dataclass
class TerminalConfig:
    width: int = CONSOLE_WIDTH
    height: int = CONSOLE_HEIGHT
    cell_width: int = HALF_TILE_SIZE
    cell_height: int = TILE_SIZE
    title: str = "Simulacra"
    font: str = "../../assets/ui_font.ttf"


class RenderManager(Manager):
    """Manager for handling the render console."""

    config = TerminalConfig()

    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self._root_console = terminal

        self._layers = {
            'BACKGROUND': 0,
            'VISIBLE': 1,
            'EXPLORED': 2,
            'ENTITY A': 10,
            'ENTITY B': 11,
            'UNKNOWN': 200,
            'INTERFACE': 220,
            }

        self._tilesets = [
            ('0xE000', "./simulacra/assets/base_tileset_saturated.png"),
            ('0xE200', "./simulacra/assets/base_tileset_desaturated.png"),
            ('0xE500', "./simulacra/assets/entity_tileset.png"),
            ('0xEF00', "./simulacra/assets/ui_tileset.png"),
            ]

        self.sprites = SpriteRegistry()

    @property
    def root_console(self):
        return self._root_console

    @property
    def layers(self):
        return self._layers

    def clear(self) -> None:
        self._root_console.clear()
        self._root_console.bkcolor(0xFFFDCBB0)

    def initialize_console(self):
        size: str = f"{self.config.width}x{self.config.height}, "
        cellsize: str = f"{self.config.cell_width}x{self.config.cell_height}, "
        title: str = f"'{self.config.title}'; "
        font: str = f"{self.config.font}"

        self._root_console.bkcolor(0xFFFDCBB0)
        self._root_console.set(f"window: size={size}")
        self._root_console.set(f"window: cellsize={cellsize}")
        self._root_console.set(f"window: title={title}")
        self._root_console.set(f"window: font: {font}")
        self._root_console.set("ui font: ./simulacra/assets/ui_font.ttf, size=10x20")
        self._root_console.set("big font: ./simulacra/assets/ui_font.ttf, size=20x40, spacing=2x2")

    def initialize_tiles(self):
        tile_config = ""

        for tileset in self._tilesets:
            tile_config += f"{tileset[0]}: {tileset[1]}, "
            tile_config += f"size={TILE_SIZE}x{TILE_SIZE}, "
            tile_config += f"align={TILE_ALIGN}, "
            tile_config += f"codepage={CODEPAGE}, "
            tile_config += f"resize={TILE_SIZE*SCALE}x{TILE_SIZE*SCALE}, "
            tile_config += f"resize-filter={RESIZE_FILTER}, "
            tile_config += f"spacing={SPACING} "
            tile_config += "; "
        self._root_console.set(tile_config)

    def setup(self):
        self._root_console.open()
        self._root_console.composition(True)

        self.initialize_console()
        self.initialize_tiles()

        self._root_console.refresh()

    def teardown(self):
        self._root_console.composition(False)
        self._root_console.close()
