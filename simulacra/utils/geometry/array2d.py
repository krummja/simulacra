from __future__ import annotations
from typing import Generic, TypeVar, Optional, List, Tuple

import numpy as np

T = TypeVar("T")


class Array2D(Generic[T]):

    def __init__(self, width: int, height: int, value: Optional[T] = None) -> None:
        self.width = width
        self.height = height
        self._elements: List[List[T]] = [ [ value for _ in range(height) ]
                                                  for _ in range(width)  ]
        self.explored = np.zeros((width, height), dtype=np.bool)
        self.visible = np.zeros((width, height), dtype=np.bool)

    @property
    def elements(self):
        return self._elements

    def __getitem__(self, key: Tuple[int, int]) -> T:
        return self._elements[key[0]][key[1]]

    def __setitem__(self, key: Tuple[int, int], value: T) -> None:
        self._elements[key[0]][key[1]] = value
