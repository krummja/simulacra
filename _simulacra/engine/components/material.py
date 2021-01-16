"""ENGINE.COMPONENTS.Material"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .component import Component

if TYPE_CHECKING:
    from engine.entities.entity import Entity


class Material(Component):
    """Material component"""

    def __init__(
            self,
            uid="<unset>",
            name="",
            hardness=0.0,
            sharpness=0.0,
            potency=0.0,
            weight=0.0,
            value=0.0
        ) -> None:
        super().__init__("MATERIAL")
        self['id'] = id
        self['name'] = name
        self['hardness'] = hardness
        self['sharpness'] = sharpness
        self['potency'] = potency
        self['weight'] = weight
        self['value'] = value

    def __str__(self) -> str:
        return f"Material({self['name']})"

    def copy(self) -> Material:
        return Material(**self)
