from __future__ import annotations

import math
import numpy as np


def vector2(x: int, y: int) -> np.ndarray:
    return np.array((x, y), dtype=np.float)

def magnitude(vec: np.ndarray) -> float:
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])

def normalize_vector(vec: np.ndarray) -> np.ndarray:
    m = magnitude(vec)
    if m > 0:
        return vec / m
