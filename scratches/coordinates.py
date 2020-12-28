from __future__ import annotations
from typing import Tuple

import math

def polar_to_cartesian(radius: float, theta: float) -> Tuple[float, float]:
    """Convert polar coordinates to cartesian coordinates."""
    x = round(radius * math.cos(theta), 2)
    y = round(radius * math.sin(theta), 2)
    return x, y


test1 = polar_to_cartesian(40.0, 60.0)
print(test1)