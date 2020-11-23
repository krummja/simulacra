from __future__ import annotations
from typing import TYPE_CHECKING

from location import Location
from graphic import Graphic
from message import Noun

if TYPE_CHECKING:
    from component import Component


class Entity(Graphic, Noun):

    ident: str = "<unset>"

    def __init__(self, location: Location) -> None:
        Graphic.__init__(self)
        Noun.__init__(self)

        self.location = location
        self.components = {}
        self.observers = {}
        self.responders = {}

    def copy_to(self, new_entity: Entity) -> Entity:
        for component in self.components.values():
            new_entity.register_component(component)
        return new_entity

    def get_component(self, component_ident: str) -> Component:
        return self.components.get(component_ident, None)

    def update(self) -> None:
        for component in self.components.values():
            component.update()

    def register_component(self, component: Component) -> None:
        if component.ident in self.components:
            self.unregister_component(component)
        self.components[component.ident] = component
        component.on_register(self)

    def unregister_component(self, component: Component) -> None:
        if component.ident in self.components:
            component.on_unregister()
            del self.components[component.ident]

    def __getitem__(self, key):
        return self.components[key]

    def __setitem__(self, key, value):
        self.components[key] = value
