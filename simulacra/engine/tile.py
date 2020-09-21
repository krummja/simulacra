from __future__ import annotations  # type: ignore
from typing import NamedTuple, Tuple, TYPE_CHECKING

import numpy as np


tile_graphic = np.dtype([
    ("ch", np.int),
    ("fg", "3B"),
    ("bg", "3B"),
])

tile_dt = np.dtype([
    ("move_cost", np.uint8),
    ("transparent", np.bool),
    ("light", tile_graphic),
    ("dark", tile_graphic),
    ("effect", tile_graphic),
])


class Tile:
    
    def __new__(
            cls,
            move_cost: int,
            transparent: bool,
            char: str,
            fg: Tuple[int, int, int],
            bg: Tuple[int, int, int]
        ) -> np.ndarray:
        instance = super(Tile, cls).__new__(cls)
        instance.__init__(move_cost, transparent, char, fg, bg)

        light = (char, fg, bg)
        dark = (char, (fg[0]//2, fg[1]//2, fg[2]//2), (bg[0]//2, bg[1]//2, bg[2]//2))
        effect = (char, fg, bg)

        return np.array(
            (move_cost, transparent, light, dark, effect),
            dtype=tile_dt
        )

    def __init__(self, move_cost, transparent, char, fg, bg) -> None:
        self.move_cost = move_cost
        self.transparent = transparent
        self.char = char
        self.fg = fg
        self.bg = bg


class _Tile(NamedTuple):
    """A NamedTuple type broadcastable to any tile_dt array."""

    move_cost: int
    transparent: bool
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]