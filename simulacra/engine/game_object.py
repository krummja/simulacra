from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

from engine.log import Noun
from engine.graphic import Graphic

if TYPE_CHECKING:
    from engine.area import Area
    from engine.model import Model
    from engine.components import Component
    from engine.location import Location


class ComponentSet(dict):

    def __init__(self: Dict[str, Component]):
        super().__init__()


class GameObject(Graphic, Noun):
    render_order = 1

    def __init__(self: GameObject, location: Location) -> None:
        Graphic.__init__(self)
        Noun.__init__(self)
        self._location = location
        self._components: ComponentSet = ComponentSet()

    @property
    def components(self: GameObject) -> ComponentSet:
        return self._components

    @property
    def location(self: GameObject) -> Location:
        return self._location

    @location.setter
    def location(self: GameObject, value: Optional[Location]) -> None:
        self._location = value

    @property
    def area(self: GameObject) -> Area:
        return self.location.area

    @property
    def model(self: GameObject) -> Model:
        return self.location.area.model

    def is_visible(self: GameObject) -> bool:
        """Whether or not this [GameObject] is currently in the player FOV."""
        return bool(self.location.area.visible[self.location.ij])
