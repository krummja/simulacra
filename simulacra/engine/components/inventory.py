from __future__ import annotations
from typing import List, TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.game_object import GameObject
    from engine.items import Item


class Inventory(Component):
    symbols: str = "abcdefghijklmnopqrstuvwxyz"
    capacity: int = len(symbols)

    def __init__(self: Inventory, game_object: GameObject) -> None:
        super().__init__(game_object)
        self._contents: List[Item] = []

    @property
    def contents(self: Inventory) -> List[Item]:
        return self._contents

    def take(self: Inventory, item: Item) -> None:
        """Take an item from its current location and put it in self."""
        assert item.owner is not self
        assert item.liftable, "You cannot take that!"
        item.lift()
        self.contents.append(item)
        item.owner = self
