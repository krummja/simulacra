from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

from bearlibterminal import terminal

from simulacra.core.options import *
from ..manager import Manager

if TYPE_CHECKING:
    from ..game import Game


@dataclass
class TerminalConfig:
    width: int = CONSOLE_WIDTH
    height: int = CONSOLE_HEIGHT
    cell_width: int = HALF_TILE_SIZE
    cell_height: int = TILE_SIZE
    title: str = "Simulacra"
    font: str = "default"


class RenderManager(Manager):
    """Manager for handling the render console."""

    config = TerminalConfig()

    def __init__(self, game: Game) -> None:
        self.game = game
        self._root_console = terminal

    @property
    def root_console(self):
        return self._root_console

    def clear(self) -> None:
        self._root_console.clear()

    def initialize_console(self):
        size: str = f"{self.config.width}x{self.config.height}, "
        cellsize: str = f"{self.config.cell_width}x{self.config.cell_height}, "
        title: str = f"'{self.config.title}'; "
        font: str = f"{self.config.font}"

        self._root_console.set(f"window: size={size}")
        self._root_console.set(f"window: cellsize={cellsize}")
        self._root_console.set(f"window: title={title}")
        self._root_console.set(f"window: font: {font}")

    def setup(self):
        self._root_console.open()
        self._root_console.composition(True)

        self.initialize_console()
        self.initialize_tiles()

        self._root_console.refresh()

    def initialize_tiles(self):
        tile_config = ""
        tile_config += f"U+E000: {TILESET_PATH}, "
        tile_config += f"size={TILE_SIZE}x{TILE_SIZE}, "
        tile_config += f"align={TILE_ALIGN}, "
        tile_config += f"codepage={CODEPAGE}, "
        tile_config += f"resize={TILE_SIZE*SCALE}x{TILE_SIZE*SCALE}, "
        tile_config += f"resize-filter={RESIZE_FILTER}, "
        tile_config += f"spacing={SPACING} "
        self._root_console.set(tile_config)

    def teardown(self):
        self._root_console.composition(False)
        self._root_console.close()
