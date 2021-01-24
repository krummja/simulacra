from __future__ import annotations

from bearlibterminal import terminal as blt
from simulacra.utils.render_utils import argb_from_color
from simulacra.core.rendering.tile_data import tile_dt
from ecstremity import Component
import numpy as np


class Tile(Component):
    name = "TILE"

    def __init__(
            self,
            char: str,
            fg: str,
            bg: str,
            transparent: bool,
            move_cost: int,
            unformed: bool
        ) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg
        self.transparent = transparent
        self.move_cost = move_cost
        self.unformed = unformed
