from __future__ import annotations  # type: ignore
from typing import NamedTuple, Tuple, TYPE_CHECKING

import numpy as np


tile_graphic = np.dtype([
    ("ch", np.int),
    ("fg", "3B"),
    ("bg", "3B")
])

tile_dt = np.dtype([
    ("move_cost", np.uint8),
    ("transparent", np.bool),
    ("light", tile_graphic),
    ("dark", tile_graphic),
])


class Tile(NamedTuple):
    """A NamedTuple type broadcastable to any tile_dt array."""

    move_cost: int
    transparent: bool
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]