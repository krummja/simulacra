from __future__ import annotations

from ecstremity import Component


class Tile(Component):

    def __init__(
            self,
            transparent: bool,
            passable: bool,
        ) -> None:
        self.transparent = transparent
        self.passable = passable
