from __future__ import annotations
from typing import TYPE_CHECKING

from component import Component
from actions import common

if TYPE_CHECKING:
    from entity import Entity


class Physics(Component):

    def __init__(
            self,
            weight: float = 0.0,
            size: str = "average",
            sharpness: float = 0.0,
            hardness: float = 0.0,
        ) -> None:
        super().__init__("PHYSICS")
        self['weight'] = weight
        self['size'] = size
        self['sharpness'] = sharpness
        self['hardness'] = hardness
        
        self.is_visible = True
        self.is_moveable = True