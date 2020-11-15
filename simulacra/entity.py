from __future__ import annotations
from typing import TYPE_CHECKING

from location import Location
from graphic import Graphic
from message import Noun

if TYPE_CHECKING:
    from component import Component


class ComponentSet(dict):

    def __init__(self, owner: Entity) -> None:
        super().__init__()
        self.owner = owner

    def add(self, component: Component) -> None:
        """Add a component by component identifier to the `Entity`."""
        self[component.ident] = component


class Entity(Graphic, Noun):

    ident: str = "<unset>"

    def __init__(self, location: Location) -> None:
        Graphic.__init__(self)
        Noun.__init__(self)

        self.location = location
        self.components = ComponentSet(self)

    def copy_to(self, new_entity: Entity):
        for component in self.components.values():
            pass
            # new_entity.components.add(component)

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value
