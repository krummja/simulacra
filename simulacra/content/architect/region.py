from __future__ import annotations
from typing import List

from engine.util import classproperty


class Region:

    def __init__(self, name: str) -> None:
        self.name = name

    @classproperty
    def everywhere(self) -> Region:
        return Region("everywhere")

    @classproperty
    def north(self) -> Region:
        return Region("north")

    @classproperty
    def northeast(self) -> Region:
        return Region("northeast")

    @classproperty
    def east(self) -> Region:
        return Region("east")

    @classproperty
    def southeast(self) -> Region:
        return Region("southeast")

    @classproperty
    def south(self) -> Region:
        return Region("south")

    @classproperty
    def southwest(self) -> Region:
        return Region("southwest")

    @classproperty
    def west(self) -> Region:
        return Region("west")

    @classproperty
    def northwest(self) -> Region:
        return Region("northwest")

    @classproperty
    def directions(self) -> List[Region]:
        return [self.north,
                self.northeast,
                self.east,
                self.southeast,
                self.south,
                self.southwest,
                self.west,
                self.northwest,
                ]
