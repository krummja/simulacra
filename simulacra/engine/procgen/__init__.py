from __future__ import annotations  # type: ignore
from typing import List, TYPE_CHECKING, Tuple

import numpy as np
from numpy import ndarray

if TYPE_CHECKING:
    from engine.area import Area
    from engine.tile import Tile


def process_map(
        area: Area, 
        base: ndarray, 
        rules: List[Tuple[str, Tile]]
    ) -> ndarray:
    """Iterate through an 1D array consisting of char strings and replace
    for Tile instances based on a supplied list of rewrite rules."""
    height: int = base.shape[0]
    row: int = 0
    for line in base:
        width: int = len(line)
        col: int = 0
        if row <= height:
            for char in line:
                if col <= width:
                    for rule in rules:
                        if char == rule[0]:
                            area.tiles[row+20, col+20] = rule[1]
                    col += 1
            row += 1
    return area