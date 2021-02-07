from __future__ import annotations

from ecstremity import Component


class ItemStack:
    def __init__(self, item) -> None:
        self.amount = 1
        self.item = item



class Inventory(Component):

    def __init__(self, openable: bool = True) -> None:
        self.openable = openable
