from __future__ import annotations
from typing import Tuple

from engine.graphic import Graphic


class Sprite(Graphic):

    def __init__(
            self: Sprite,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int]
         ) -> None:
        self.char = char
        self.color = color
        self.bg = bg
