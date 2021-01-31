from __future__ import annotations

from ecstremity import Component


class Tile(Component):
    name = "TILE"

    def __init__(
            self,
            transparent: bool,
            move_cost: int,
            unformed: bool
        ) -> None:
        self.transparent = transparent
        self.move_cost = move_cost
        self.unformed = unformed
