from __future__ import annotations
from typing import List, Generator, Tuple

import numpy as np
import tcod


class CharacterMap:

    def __init__(self) -> None:
        self._data: List[int] = tcod.tileset.CHARMAP_CP437
        _pua_start: int = 57344
        _pua_end: int = 57856
        self._data.extend(range(_pua_start, _pua_end))

    @property
    def data(self) -> List[int]:
        return self._data

    @property
    def as_array(self) -> np.ndarray:
        return np.array(self._data, dtype=np.int).reshape(32, 16)

    @property
    def enumerated(self) -> Generator[Tuple[int, int], None, None]:
        for count, value in enumerate(self._data):
            yield (count, value)


TILESET = tcod.tileset.load_tilesheet(
    path="./simulacra/assets/Simulacra_20x20.png",
    columns=16,
    rows=32,
    charmap=CharacterMap().data
    )
