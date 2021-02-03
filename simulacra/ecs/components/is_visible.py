from __future__ import annotations

from ecstremity import Component


class IsVisible(Component):
    name = "IS_VISIBLE"

    def __init__(self, amount: int = 0, distance: int = 0) -> None:
        self.amount = amount
        self.distance = distance
