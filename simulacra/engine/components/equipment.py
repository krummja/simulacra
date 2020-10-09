from __future__ import annotations
from typing import List, TYPE_CHECKING

from engine.components import Component

if TYPE_CHECKING:
    from engine.game_object import GameObject
    from engine.items import Item, Tuple


class Slot:
    location: str = ""
    content: Item


class Equipment(Component):

    def __init__(self: Equipment, owner: GameObject) -> None:
        super().__init__(owner)

    @property
    def contents(self: Equipment) -> List[Item]:
        contents = []
        return contents

    def take(self: Equipment, item: Item) -> None:
        """Take an item from its current location and put it in self."""
        assert item.owner is not self
        assert item.liftable, "You cannot take that!"
        item.lift()
        # self.contents.append(item)
        # item.owner = self
