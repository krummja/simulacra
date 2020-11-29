from __future__ import annotations
from typing import TYPE_CHECKING

from location import Location
from graphic import Graphic
from message import Noun

if TYPE_CHECKING:
    from component import Component


class Entity(Graphic, Noun):

    NAME: str = "<unset>"

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

    def get_component(self, component_name: str) -> Component:
        return self.components.get(component_name, None)

    def update(self) -> None:
        for component in self.components.values():
            component.update()

    def register_component(self, component: Component) -> None:
        if component.NAME in self.components:
            self.unregister_component(component)
        self.components[component.NAME] = component
        component.on_register(self)

    def unregister_component(self, component: Component) -> None:
        if component.NAME in self.components:
            component.on_unregister()
            del self.components[component.NAME]

    def attach_observer(self, observer) -> None:
        self.observers[observer.name] = observer