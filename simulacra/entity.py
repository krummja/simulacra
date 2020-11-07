from __future__ import annotations
from typing import TYPE_CHECKING

from location import Location
from graphic import Graphic
from message import Noun

if TYPE_CHECKING:
    from component import Component


class ComponentSet(dict):

    def __init__(self, entity: Entity) -> None:
        super().__init__()
        self.entity = entity

    def add(self, component: Component) -> None:
        self[f"{component.ident}"] = component


class Entity(Graphic, Noun):

    def __init__(self, location: Location) -> None:
        Graphic.__init__(self)
        Noun.__init__(self)

        self.location = location
        self.components = ComponentSet(self)

    def __getitem__(self, key):
        return self.components[key].data
