from __future__ import annotations
from typing import Generic, TypeVar, Optional, List, Tuple

import math
import numpy as np

T = TypeVar("T")


class Array2D(Generic[T]):

    def __init__(self, width: int, height: int, value: Optional[T] = None) -> None:
        self._width = width
        self._height = height
        self._elements: List[List[T]] = [ [ value for _ in range(self._width)  ]
                                                  for _ in range(self._height) ]

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def elements(self):
        return self._elements

    def __getitem__(self, key: Tuple[int, int]) -> T:
        return self._elements[key[0]][key[1]]

    def __setitem__(self, key: Tuple[int, int], value: T) -> None:
        self._elements[key[0]][key[1]] = value
