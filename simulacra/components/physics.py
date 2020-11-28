from __future__ import annotations
from typing import TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from entity import Entity


class Physics(Component):

    ident = "PHYSICS"

    def __init__(
            self,
            weight: float = 0.0,
            size: str = "average",
            sharpness: float = 0.0,
            hardness: float = 0.0,
        ) -> None:
        super().__init__()
        self.weight = weight
        self.size = size
        self.sharpness = sharpness
        self.hardness = hardness
        
    def __repr__(self):
        return str(vars(self))