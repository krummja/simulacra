from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from engine.log import Noun
from engine.sprite import Sprite

if TYPE_CHECKING:
    from engine.area import Area
    from engine.model import Model
    from engine.components import Component
    from engine.location import Location


class ComponentSet(dict):

    def __init__(self: Dict[str, Component]):
        super().__init__()


class GameObject(Sprite, Noun):
    """
    The [GameObject] class is the primary representation of A Thing in the
    game world. It extends the [Sprite] class which provides its graphical
    data, and the [Noun] class which provides its descriptive data.

    On top of these, the [GameObject] introduces properties for [Location]
    and [ComponentSet], both of which are fundamental for defining the basic
    characteristics of an object in the game.
    """

    def __init__(
            self: GameObject,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            ) -> None:
        Sprite.__init__(self, char, color, bg)
        Noun.__init__(self, noun_text)
        self._components: ComponentSet = ComponentSet()
        self._location: Optional[Location] = None

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
