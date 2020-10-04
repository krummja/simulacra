from __future__ import annotations
from typing import Optional, Tuple, Type, TYPE_CHECKING

from engine.actions import ActionWithItem, Impossible
from engine.actions.behaviors import Behavior
from engine.actor import Actor
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
            location: Location,
            equippable: bool,
        ) -> None:
        super().__init__(char, color, bg, noun_text, location)
        self.equippable = equippable
        self.owner: Optional[Inventory] = None
        self.suffix = ""
        self.liftable: bool = False

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

    def place(self: Item, location: Location):
        """Place this item on the floor at the given location."""
        assert not self.location, "This item already has a location."
        assert not self.owner, "Can't be placed because it is currently owned."
        self.location = location
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

    @classmethod
    def spawn(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            equippable: bool,
        ) -> Item:
        self = cls(char, color, bg, noun_text, location, equippable)
        self.liftable = True
        try:
            location.area.items[location.xy].append(self)
        except KeyError:
            location.area.items[location.xy] = [self]
        return self

    @classmethod
    def spawn_actor(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            behavior: Optional[Type[Behavior]],
            equippable: bool,
        ) -> Actor:
        self = cls(char, color, bg, noun_text, location, equippable)
        self.liftable = False
        actor = Actor(location, self, behavior)
        self.location.area.actors.add(actor)
        return actor
