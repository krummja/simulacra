from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from content.tiles import font_map
from engine.items import Item
from engine.components.offense import Offense

if TYPE_CHECKING:
    from engine.location import Location


class Weapon(Item):

    def __init__(
            self: Weapon,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            equippable: bool,
        ) -> None:
        Item.__init__(
            self,
            char,
            color,
            bg,
            noun_text,
            location,
            equippable,
            )
        self.offense = Offense(self)


weapons = {
    'basic sword': {
        'char': font_map['barrel_01'],
        'color': (255, 0, 0),
        'bg': (0, 0, 0),
        'noun_text': 'Basic Sword'
        }
    }
