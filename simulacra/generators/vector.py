from __future__ import annotations
from typing import Tuple

import math


def magnitude(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def dot(a, b):
    return sum(i * j for i, j in zip(a, b))


def angle_between(a, b):
    return math.degrees(math.acos(dot(a, b) / (magnitude(*a) * magnitude(*b))))


def limit_magnitude(vector, max_magnitude, min_magnitude = 0.0):
    mag = magnitude(*vector)
    if mag > max_magnitude:
        normalizing_factor = max_magnitude / mag
    elif mag < min_magnitude:
        normalizing_factor = min_magnitude / mag
    else: return vector
    
    return [value * normalizing_factor for value in vector]
    