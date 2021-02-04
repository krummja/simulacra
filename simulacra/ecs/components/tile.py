from __future__ import annotations

from ecstremity import Component


class Tile(Component):
    name = "TILE"

    def __init__(
            self,
            transparent: bool,
            passable: bool,
            unformed: bool
        ) -> None:
        self.transparent = transparent
        self.passable = passable
        self.unformed = unformed
