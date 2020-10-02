from __future__ import annotations
from typing import Tuple

import numpy as np

from engine.graphic import Graphic


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
    ])


class Tile(Graphic):

    def __new__(
            cls,
            move_cost: int,
            transparent: bool,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int]
        ) -> np.ndarray:
        instance = super(Tile, cls).__new__(cls)
        instance.__init__(move_cost, transparent, char, color, bg)

        light = (char, color, bg)
        dark = (char, color, bg)

        return np.array((move_cost, transparent, light, dark), dtype=tile_dt)

    def __init__(
            self: Tile,
            move_cost: int,
            transparent: bool,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int]
        ) -> None:
        self.move_cost = move_cost
        self.transparent = transparent
        self.char = char
        self.color = color
        self.bg = bg
