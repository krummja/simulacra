from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

from engine.actions import ActionWithItem, Impossible
from engine.game_object import GameObject
from engine.location import Location

if TYPE_CHECKING:
    from engine.components.inventory import Inventory


class Item(GameObject):

    def __init__(
            self: Item,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location
        ) -> None:
        super().__init__(char, color, bg, noun_text)
        self._equippable: bool = False
        self._liftable: bool = False
        self._owner: Optional[Inventory] = None
        self._suffix = ""
        self._location = location

    @property
    def equippable(self: Item) -> bool:
        return self._equippable

    @equippable.setter
    def equippable(self: Item, value: bool) -> None:
        self._equippable = value

    @property
    def liftable(self: Item) -> bool:
        return self._liftable

    @liftable.setter
    def liftable(self: Item, value: bool) -> None:
        self._liftable = value

    @property
    def owner(self: Item) -> Inventory:
        return self._owner

    @owner.setter
    def owner(self: Item, value: Inventory) -> None:
        self._owner = value

    @property
    def suffix(self: Item) -> str:
        return self._suffix

    @suffix.setter
    def suffix(self: Item, value: str) -> None:
        self._suffix = value

    def lift(self: Item) -> None:
        """Remove this item from any of its containers."""
        if self.owner:
            self.owner.contents.remove(self)
            self.owner = None
        if self.location:
            item_list = self.location.area.items[self.location.xy]
            item_list.remove(self)
            if not item_list:
                del self.location.area.items[self.location.xy]
            self.location = None

    @classmethod
    def place(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location
        ) -> None:
        """Place this item on the floor at the given location."""
        self = cls(char, color, bg, noun_text, location)
        assert not self.owner, "Can't be placed because it is currently owned."
        items = location.area.items
        try:
            items[location.xy].append(self)
        except KeyError:
            items[location.xy] = [self]

    def plan_activate(self: Item, action: ActionWithItem) -> ActionWithItem:
        return action

    def action_activate(self: Item, action: ActionWithItem) -> None:
        raise Impossible(f"You can do nothing with the {self.noun_text}")

    def consume(self: Item, action: ActionWithItem) -> None:
        """Remove this item from the actor's inventory."""
        assert action.item is self
        action.item.lift()

    def action_drink(self: Item, action: ActionWithItem) -> None:
        """Drink this."""
        raise Impossible(f"You can't drink the {self.noun_text}")
