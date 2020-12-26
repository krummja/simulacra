from __future__ import annotations
from typing import (Dict, 
                    List, 
                    Tuple,
                    Union)

import numpy as np
import tcod


class Tilemap:
    """Class representing the tilemap unicode codepoints.
    
    I extend the base Codepage 437 character map with a region of the Unicode
    Private Use Area (thanks to HexDecimal for tipping me off to the PUA!) for
    custom glyphs.
    """
    
    def __init__(self) -> None:
        self.PUA_START: int = 57344
        self.EXTENSION: int = 512
        self.PUA_END = self.PUA_START + self.EXTENSION
        self._charmap = tcod.tileset.CHARMAP_CP437
        self._charmap.extend([_ for _ in range(self.PUA_START, self.PUA_END)])
        
    @property
    def charmap(self) -> List[int]:
        """The list of integers defining the available Unicode codepoints."""
        return self._charmap
    
    @property
    def charmap_indices(self) -> List[int]:
        """A straightforward enumeration of all of the number of available
        codepoint positions. This is useful for mapping in prefabricated maps
        from Tiled.
        """
        return [_ for _ in range(len(self._charmap))]
    
    @property
    def shape(self) -> Tuple[int, int]:
        """Calculate the width and height of the charmap for use elsehwere."""
        return (len(self.charmap) // 16, 16)
    
    @property
    def tilesheet(self) -> tcod.tileset.Tileset:
        """Loaded tilesheet to be used during window setup."""
        return tcod.tileset.load_tilesheet(
            path="./simulacra/assets/simulacra16x16_2.png",
            columns=self.shape[1],
            rows=self.shape[0],
            charmap=self.charmap
            )
    
    @property
    def charmap_array(self) -> np.ndarray:
        return np.array(self.charmap, dtype=np.int).reshape(self.shape)
    
    @property
    def indices_array(self) -> np.ndarray:
        return np.array(self.charmap_indices, dtype=np.int).reshape(self.shape)
