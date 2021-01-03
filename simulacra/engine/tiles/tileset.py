from __future__ import annotations
from typing import TYPE_CHECKING

from collections import defaultdict
from enum import Enum

if TYPE_CHECKING:
    from engine.tiles.glyphset import GlyphSet


class BareTile(Enum):
    Unformed = 0
    UnformedWet = 1
    Open = 2
    Solid = 3
    Passage = 4
    Doorway = 5
    SolidWet = 6
    PassageWet = 7

class TileType(Enum):
    Wall = 0
    Floor = 1


class TileSet(defaultdict):
    """Array of tile data built from a GlyphSet."""

    def __init__(
            self, *,
            uid: str,
            tile_type: TileType,
            glyphset: GlyphSet
        ) -> None:
        """Constructor.

        Take in a UID slug, TileType, and GlyphSet instance.
        Constructs a TileSet dictionary encoding UIDs for each glyph, the `move_cost` and
        `transparent` properties of the tiles, and a character for each tile.

        e.g. 'brick_wall', TileType.Wall, BRICK_WALL_GS
             -> {'brick_wall_W': {
                    'move_cost': TileType.Wall,
                    'transparent': TileType.Wall,
                    'char': 57376
                    }}

        The TileSet instance can then be used to build TileSetVariant objects by
        specifying foreground and background colors.

        Access a specific TileSet template by indexing the TileSet instance with
        the tile UID, e.g. BRICK_WALL['brick_wall_W']
        """
        super().__init__()
        self.uid = uid
        self._tile_type = tile_type
        self._glyphset = glyphset

        for suffix, glyph in self._glyphset.uid_map:
            self[self.uid + '_' + suffix] = {
                'move_cost': self._tile_type,
                'transparent': self._tile_type,
                'char': glyph
                }
