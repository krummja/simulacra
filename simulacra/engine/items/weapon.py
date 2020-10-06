from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from content.tiles import font_map
from engine.items import Item
from engine.components.offense import Offense

if TYPE_CHECKING:
    from engine.location import Location


class Weapon(Item):

    def __init__(
            self: Item,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location
        ) -> None:
        Item.__init__(self, char, color, bg, noun_text, location)
        self.equippable = True
        self.liftable = True
        self.owner = None
        self.suffix = ""
        self.components['OFFENSE'] = Offense(self)


class Sword(Weapon):

    def __init__(
            self: Sword,
            char: str,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location
        ) -> None:
        Weapon.__init__(self, char, color, bg, noun_text, location)
        self.equippable = True
        self.liftable = True
        self.owner = None
        self.suffix = ""
