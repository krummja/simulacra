from __future__ import annotations
from typing import List, TYPE_CHECKING, Tuple

from numpy import ndarray
from engine.items.door import Door
from engine.hues import COLOR
from content.tiles import font_map

if TYPE_CHECKING:
    from engine.area import Area
    from engine.tile import Tile


def process_map(
        area: Area,
        base: ndarray,
        rules: List[Tuple[str, Tile]]
    ) -> Area:
    """Iterate through an 1D array consisting of char strings and replace
    for Tile instances based on a supplied list of rewrite rules."""
    height: int = base.shape[0]
    base_row: int = 0
    for line in base:
        width: int = len(line)
        base_col: int = 0
        if base_row <= height:
            for char in line:
                if base_col <= width:
                    for rule in rules:
                        if char == rule[0]:
                            area.tiles[base_row+20, base_col+20] = rule[1]
                    base_col += 1
            base_row += 1

    return area


def process_doors(doors: ndarray) -> List[Tuple[int, int]]:

    door_list = []
    height: int = doors.shape[0]
    door_row: int = 0
    for line in doors:
        width: int = len(line)
        door_col: int = 0
        if door_row <= height:
            for char in line:
                if door_col <= width:
                    if char == 'D':
                        door_list.append((door_row + 20, door_col + 20))
                    door_col += 1
            door_row += 1
    return door_list
