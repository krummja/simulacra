from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from engine.items import Item
from content.tiles import font_map

if TYPE_CHECKING:
    from engine.location import Location


class OpenableState:

    _is_open: bool

    @property
    def is_open(self: OpenableState) -> bool:
        return self._is_open

    @is_open.setter
    def is_open(self: OpenableState, value: bool) -> None:
        self._is_open = value


class Door(Item, OpenableState):

    closed_sprite: int = font_map['door_01']
    open_sprite: int = font_map['door_02']

    def __init__(
            self: Door,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            carryable: bool,
            equippable: bool
        ) -> None:
        super().__init__(
            char,
            color,
            bg,
            noun_text,
            location,
            carryable,
            equippable
            )

    def mut_state(self: Door) -> None:
        if self.is_open is True:
            self.is_open = False
            self.location.area.model.report(f"{self.noun_text} swings shut.")
            self.char = self.closed_sprite
        if self.is_open is False:
            self.is_open = True
            self.location.area.model.report(f"{self.noun_text} creaks open.")
            self.char = self.open_sprite
