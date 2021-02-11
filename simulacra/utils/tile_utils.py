from __future__ import annotations
from typing import Generic, TypeVar
import numpy as np
from collections import deque


DType = TypeVar("DType")
class Array(np.ndarray, Generic[DType]):
    """Dummy class for type annotating NumPy ndarrays."""


def bitmask_to_decimal(arg):
    "Bitmask-to-Base10 values for the corresponding tile index."
    switch = {
          2 : 1,
          8 : 2,
         10 : 3,
         11 : 4,
         16 : 5,
         18 : 6,
         22 : 7,
         24 : 8,
         26 : 9,
         27 : 10,
         30 : 11,
         31 : 12,
         64 : 13,
         66 : 14,
         72 : 15,
         74 : 16,
         75 : 17,
         80 : 18,
         82 : 19,
         86 : 20,
         88 : 21,
         90 : 22,
         91 : 23,
         94 : 24,
         95 : 25,
        104 : 26,
        106 : 27,
        107 : 28,
        120 : 29,
        122 : 30,
        123 : 31,
        126 : 32,
        127 : 33,
        208 : 34,
        210 : 35,
        214 : 36,
        216 : 37,
        218 : 38,
        219 : 39,
        222 : 40,
        223 : 41,
        248 : 42,
        250 : 43,
        251 : 44,
        254 : 45,
        255 : 46,
          0 : 47,
        }
    return switch.get(arg, 0)


walkable = np.array([
    [0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 1, 0, 0],
    ])


def generate_bitmask(walkable: Array[bool]) -> Array[int]:
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, -1)]

