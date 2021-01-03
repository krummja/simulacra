"""ENGINE.RENDERING.Tilemap"""
from __future__ import annotations
from typing import List, Generator, Tuple

import numpy as np
import tcod

from engine.util import Singleton


class TilesetData(metaclass=Singleton):

    def __init__(self) -> None:
        self._charmap: List[int] = tcod.tileset.CHARMAP_CP437
        _pua_start: int = 57344
        _pua_end: int = 57856
        self._charmap.extend(range(_pua_start, _pua_end))

    @property
    def charmap(self) -> List[int]:
        """The extended CP437 charmap, extended with 512 codepoints from the
        unicode private use area (codepoints 57344:57856)
        """
        return self._charmap

    @property
    def charmap_array(self) -> np.ndarray:
        return np.array(self._charmap, dtype=np.int).reshape(80, 16)

    @property
    def tilemap(self) -> Generator[Tuple[int, int], None, None]:
        """A list of integers starting from 0 representing the Tiled-generated
        tilemap enumeration.
        """
        for count, value in enumerate(self._charmap):
            yield (count, value)


tileset = tcod.tileset.load_tilesheet(
    path="./simulacra/assets/simulacra16x16_2.png",
    columns=16,
    rows=48,
    charmap=TilesetData().charmap)
