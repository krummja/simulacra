from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

import numpy as np

from content.architect.array2d import Array2D
from engine.geometry.point import Point
from engine.geometry.rect import Rect
from engine.geometry.span import Span
from engine.tiles.tileset import BareTile

if TYPE_CHECKING:
    from engine.areas.area import Area
    from engine.model import Model
    from engine.tiles.tile import Tile
    from content.architect.architecture import Architecture


class Architect:
    """The main class that orchtestrates painting and populating the area."""

    def __init__(self, area: Area, depth: int) -> None:
        self.area = area
        self.depth = depth
        self._bounds = Rect.from_spans(
            horizontal=Span(0, area.width),
            vertical=Span(0, area.height))
        self._owners: Array2D[Architecture] = Array2D(shape=(area.width, area.height))
        self._carved_tiles: int = 0

    def build_area(self, set_player_start: Callable[[Point], None]) -> Area:
        unowned_passages: List[str] = []

    def owner_at(self, pos: Point) -> Architecture:
        return self._owners[pos]

    def _carve(self, architecture: Architecture, x: int, y: int, tile: Tile) -> None:
        pass

    def _can_carve(self, architecture: Architecture, pos: Point) -> bool:
        if pos in self._bounds:
            return False
        if self._owners[pos] is not None:
            return False

        # water checker

        for here in pos.neighbors:
            if here in self._bounds:
                continue
            # water checker for neighbor
            owner = self._owners[here]
            if owner is not None and owner != architecture:
                return False
        return True

    def _fill_passages(self):
        pass

    def _add_shortcuts(self):
        pass

    def _try_shortcut(self):
        pass

    def _is_shortcut(self):
        pass

    def _make_passage(self):
        pass

    def _claim_passages(self):
        pass

    def _claim_neighbors(self, pos: Point, owner: Architecture) -> None:
        pass

    def _is_formed(self) -> bool:
        pass

    def _is_open_at(self) -> bool:
        pass

    def _is_solid_at(self) -> bool:
        pass
