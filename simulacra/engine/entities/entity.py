"""ENGINE.ENTITIES.Entity"""
from __future__ import annotations

from typing import TYPE_CHECKING

from engine.areas import Location
from engine.entities.noun import Noun
from engine.rendering import Graphic

if TYPE_CHECKING:
    from engine.components.component import Component


class Entity(Graphic, Noun):
    """An `Entity` is a primary game object that is basically a blank wrapper
    for a set of `Component`s."""

    def __init__(self, uid: str, location: Location) -> None:
        Graphic.__init__(self)
        Noun.__init__(self)
        self.uid = uid
        self.location = location
        self.components = {}

    @property
    def noun_text(self) -> str:
        return self._noun_text

    def copy_to(self, new_entity: Entity) -> Entity:
        """Make a copy of this `Entity` with all components registered."""
        for component in self.components.values():
            new_entity.register_component(component)
        return new_entity

    def register_component(self, component: Component) -> None:
        """Add a `Component` to this `Entity`'s component dict."""
        if component.uid in self.components:
            self.unregister_component(component)
        self.components[component.uid] = component
        component.on_register(self)

    def unregister_component(self, component: Component) -> None:
        """Remove a `Component` from this `Entity`'s component dict."""
        if component.uid in self.components:
            component.on_unregister()
            del self.components[component.uid]
