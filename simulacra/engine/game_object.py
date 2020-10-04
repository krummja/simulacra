from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from engine.log import Noun
from engine.sprite import Sprite

if TYPE_CHECKING:
    from engine.components import Component
    from engine.location import Location


class ComponentSet(dict):

    def __init__(self: Dict[str, Component]):
        super().__init__()


class GameObject(Sprite, Noun):

    def __init__(
            self: GameObject,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            ) -> None:
        Sprite.__init__(self, char, color, bg)
        Noun.__init__(self, noun_text)
        self._components: ComponentSet = ComponentSet()
        self._location = location

    @property
    def components(self: GameObject) -> ComponentSet:
        return self._components

    @property
    def location(self: GameObject) -> Location:
        return self._location

    @location.setter
    def location(self: GameObject, value: Optional[Location]) -> None:
        self._location = value

    def is_visible(self: GameObject) -> bool:
        return bool(self.location.area.visible[self.location.ij])
