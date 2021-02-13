from __future__ import annotations

from ecstremity import Component


class Tile(Component):

    def __init__(
            self,
            transparent: bool = True,
            passable: bool = True,
        ) -> None:
        self.transparent = transparent
        self.passable = passable
