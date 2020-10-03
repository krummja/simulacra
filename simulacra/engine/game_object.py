from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from engine.log import Noun
from engine.sprite import Sprite

if TYPE_CHECKING:
    from engine.location import Location


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
        self._location = location

    @property
    def location(self: GameObject) -> Location:
        return self._location

    def is_visible(self: GameObject) -> bool:
        return bool(self.location.area.visible[self.location.ij])
