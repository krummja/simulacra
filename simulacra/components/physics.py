from __future__ import annotations
from typing import TYPE_CHECKING

from component import Component
from actions import common

if TYPE_CHECKING:
    from entity import Entity


class Physics(Component):

    NAME = "PHYSICS"

    def __init__(
            self,
            weight: float = 0.0,
            size: str = "average",
            sharpness: float = 0.0,
            hardness: float = 0.0,
        ) -> None:
        super().__init__()
        self._data['weight'] = weight
        self._data['size'] = size
        self._data['sharpness'] = sharpness
        self._data['hardness'] = hardness
        
        self.is_visible = True
        self.is_moveable = True