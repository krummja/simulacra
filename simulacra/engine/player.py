from __future__ import annotations
from typing import Optional, Tuple, Type, TYPE_CHECKING

from engine.game_object import GameObject
from engine.actor import Actor

if TYPE_CHECKING:
    from engine.actions.behaviors import Behavior
    from engine.location import Location


class Player(GameObject):

    def __init__(
            self: Player,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
        ) -> None:
        super().__init__(char, color, bg, noun_text, location)

    @classmethod
    def spawn(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            behavior: Optional[Type[Behavior]]
        ) -> Actor:
        self = cls(char, color, bg, noun_text, location)
        return Actor(location, self, behavior)
