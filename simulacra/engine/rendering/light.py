from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING


class Light:
    
    def __init__(self, x, y, z, r, g, b, strength) -> None:
        self.x, self.y, self.z = x, y, z
        self.r, self.g, self.b = r, g, b
        self.strength = strength