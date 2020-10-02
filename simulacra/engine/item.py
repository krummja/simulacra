from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from engine.game_object import GameObject

if TYPE_CHECKING:
    from engine.location import Location


class Item(GameObject):

    def __init__(
            self: Item,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            carryable: bool,
            wearable: bool,
        ) -> None:
        super().__init__(char, color, bg, noun_text, location)
        self.is_carryable = carryable
        self.is_wearable = wearable

    def __repr__(self: Item) -> str:
        return f"{self.__class__.__name__}({self.location!r})"
