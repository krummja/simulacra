from __future__ import annotations  # type: ignore
from typing import Optional, TYPE_CHECKING

from engine.graphic import Graphic

from engine.actions import Impossible

if TYPE_CHECKING:
    from engine.actions import ActionWithItem
    from engine.location import Location
    from engine.inventory import Inventory


class Item(Graphic):
    render_order = 1

    def __init__(self) -> None:
        self.owner: Optional[Inventory] = None
        self.location: Optional[Location] = None

    def lift(self) -> None:
        """Remove this item from any of its container."""
        if self.owner:
            self.owner.contents.remove(self)
            self.owner = None
        if self.location:
            item_list = self.location.area.items[self.location.xy]
            item_list.remove(self)
            if not item_list:
                del self.location.area.items[self.location.xy]
            self.location = None

    def place(self, location: Location) -> None:
        """Place this item on the floor at the given location."""
        assert not self.location, "This item already has a location."
        assert not self.owner, "This can't be placed because this item is currently owned."
        self.location = location
        items = location.area.items
        try:
            items[location.xy].append(self)
        except KeyError:
            items[location.xy] = [self]

    def plan_activate(self, action: ActionWithItem) -> ActionWithItem:
        """Item activated as part of an action.
        
        Assume that action has an actor which is holding this item's entity.
        """
        return action

    def action_activate(self, action: ActionWithItem) -> None:
        raise Impossible(f"You can do nothing with the {self.name}")

    def consume(self, action: ActionWithItem) -> None:
        """Remove this item from the actor's inventory."""
        assert action.item is self
        action.item.lift()

    def action_drink(self, action: ActionWithItem):
        """Drink this item."""
        raise Impossible("You can't drink that.")