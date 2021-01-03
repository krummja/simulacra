from __future__ import annotations
from typing import List, Tuple

from enum import Enum
import numpy as np

from engine.tiles.tilemap import TilesetData


class GlyphsetType(Enum):
    Glyph = 0
    HRow = 1
    VRow = 2
    Array = 3
    Enumerate = 4


class GlyphSet:
    """Array of glyph data organized into a grid."""

    def __init__(
            self, *,
            glyphset_type: GlyphsetType,
            index: np.IndexExpression
        ) -> None:
        """Constructor.

        Take in a GlyphsetType and a NumPy IndexExpression.
        Constructs a list of UID suffixes based on the GlyphsetType and stores the
        indexed portion of the character map as a glyphmap.

        e.g. GlyphsetType.Row, np.s_[18, 0:2]
             -> uid_list = ['W',   'M',   'E']
             -> glyphmap = [57376, 57377, 57378]

        The uid_map property zips the two lists together.

        The GlyphSet object can be used to build a TileSet dict, where the TileSet UID
        acts as a slug for the GlyphSet uid list.
        """
        self._index = index
        self._data = TilesetData().charmap_array[self._index]

        if glyphset_type == GlyphsetType.Glyph:
            self.uid_list = [ '' ]
        elif glyphset_type == GlyphsetType.HRow:
            self.uid_list = [ 'W', 'M', 'E' ]
        elif glyphset_type == GlyphsetType.VRow:
            self.uid_list = [ 'N', 'M', 'S' ]
        elif glyphset_type == GlyphsetType.Array:
            self.uid_list = [ 'NW', 'N', 'NE',
                              'W',  'M', 'E',
                              'SW', 'S', 'SE' ]
        elif glyphset_type == GlyphsetType.Enumerate:
            self.uid_list = list(str(i) for i in range(len(self._data)))

    @property
    def glyphmap(self) -> np.ndarray:
        return self._data

    @property
    def uid_map(self) -> List[Tuple[str, int]]:
        return list(zip(self.uid_list,
                        self.glyphmap.ravel()))
