from __future__ import annotations
from typing import Generic, TypeVar, Tuple

import numpy as np

from engine.geometry.point import Point
from engine.tiles.tile import Tile, tile_dt

T = TypeVar("T")


class Array2D(Generic[T]):
    """Helper class that abstracts over a two-dimensional array. Useful for
    applying generators to area tiles."""

    def __init__(self, shape: Tuple[int, int]) -> None:
        self.shape = shape
        self.width = shape[0]
        self.height = shape[1]
        self.tiles = np.full(shape, fill_value=0, order="F", dtype=tile_dt)

    def generated(self, shape: Tuple[int, int], generator) -> None:
        self.width = shape[0]
        self.height = shape[1]
        self.tiles = np.full(shape, fill_value=0, order="F", dtype=tile_dt)

    def generate(self, generator) -> None:
        """Evaluates [generator] at each position in the array and sets the
        element at that position to the result.
        """
        for row in self.array[:]:
            for pos in row:
                generator(pos)

    def get_at_pos(self, pos: Point) -> T:
        """Get the element in the array at [pos]."""
        return self.array[pos.xy]

    def set_at_pos(self, pos: Point, value: T) -> None:
        """Set the element in the array at [pos] to [value]."""
        self.array[pos.xy] = value

    def fill(self, value: T) -> None:
        """Set every element in the array to [value]."""
        self.array = np.full((self.width, self.height), fill_value=value, order="F")

    def __getitem__(self, pos: Point) -> Tile:
        return self.tiles[pos]
