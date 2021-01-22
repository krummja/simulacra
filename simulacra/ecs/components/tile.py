from __future__ import annotations

from simulacra.core.rendering.tile_data import tile_dt
from ecstremity import Component
import numpy as np


class Tile(Component):
    name = "TILE"

    def __init__(self, move_cost: int, transparent: bool, char: str, color, bg) -> None:
        self.move_cost = move_cost
        self.transparent = transparent
        self.char = char
        self.color = color
        self.bg = bg

        self.light = (char, color, bg)
        self.dark = (char,
                     (color[0] // 2, color[1] // 2, color[2] // 2),
                     (bg[0] // 2, bg[1] // 2, bg[2] // 2))

    @property
    def data(self):
        return np.array(
            (self.move_cost, self.transparent, self.light, self.dark), dtype=tile_dt)
