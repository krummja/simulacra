from __future__ import annotations
from typing import TYPE_CHECKING

from component import Component
from attribute import Attribute

if TYPE_CHECKING:
    from entity import Entity


class Attributes(Component):

    # TODO: Complete this component.
    def __init__(self, owner: Entity) -> None:
        super().__init__(owner)

        self['HEALTH'] = Attribute(owner, 'health', 10)
        self['ENERGY'] = Attribute(owner, 'energy', 10)
        self['HUNGER'] = Attribute(owner, 'hunger', 10)
        # self['EXPERIENCE'] = Attribute(owner, 'experience', 1)

    def configure(self) -> None:
        pass
