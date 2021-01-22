from __future__ import annotations
from typing import NamedTuple, Tuple

from .tile_data import tile_dt, tile_graphic


class TileGraphic(NamedTuple):
    char: int
    color: Tuple[int, int, int]
    bg: Tuple[int, int, int]
    render_order: int = 0
