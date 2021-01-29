from __future__ import annotations

from ecstremity import Component


class Tile(Component):
    name = "TILE"

    def __init__(
            self,
            char: str,
            fg: str,
            bg: str,
            transparent: bool,
            move_cost: int,
            unformed: bool
        ) -> None:
        self.char = char
        self.fg = fg
        self.bg = bg
        self.transparent = transparent
        self.move_cost = move_cost
        self.unformed = unformed
