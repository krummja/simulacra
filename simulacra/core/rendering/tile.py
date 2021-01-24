from __future__ import annotations
import dataclasses
from typing import NamedTuple, Tuple
from dataclasses import dataclass

from .tile_data import tile_dt, tile_graphic


@dataclass
class Tile:
    char: int
    color: str = "white"
    bg: str = "black"
    render_order: int = 0
