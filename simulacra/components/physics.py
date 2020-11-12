from __future__ import annotations
from typing import TYPE_CHECKING

from component import Component

if TYPE_CHECKING:
    from entity import Entity


class Physics(Component):

    ident = "PHYSICS"

    def __init__(self, owner: Entity) -> None:
        super().__init__(owner)
        self['WEIGHT'] = 0
        self['MOVABLE'] = True

    def configure(self, weight: int) -> None:
        self['WEIGHT'] = weight
        if self['WEIGHT'] == -1:
            self['MOVABLE'] = False
        else:
            self['MOVABLE'] = True
