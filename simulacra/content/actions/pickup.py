from __future__ import annotations
from typing import TYPE_CHECKING

from engine.events import Action, ActionWithItem, Impossible, message as message


class Pickup(Action):
    """Remove an item from a nearby tile and place it in the player's
    inventory component.
    """

    def plan(self) -> Action:
        if not self.area.items.get(self.location.xy):
            self.success = False
            self.message = message.Message("There is nothing to pick up.")
            raise Impossible(self)
        return self

    def act(self) -> Action:
        for item in self.area.items[self.location.xy]:
            try:
                self.success = True
                self.message = message.Message(f"{0} pick[s] up the {1} and stow[s] "
                                       f"{1, message.THEM}.",
                                       noun1=self.actor.owner,
                                       noun2=item)
                item.lift()
                self.actor.owner.components['INVENTORY'].add_item(item)
                self.actor.reschedule(100)
                return self
            except Impossible(self):
                self.success = False
                self.message = message.Message(f"{0} cannot lift the {1}!",
                                       noun1=self.actor.owner,
                                       noun2=item)
                raise


class Drop(ActionWithItem):
    """Remove an item from inventory and place on the ground."""

    def act(self) -> Action:
        assert self.item in self.model.player.components['INVENTORY']['item_stacks'].keys()
        self.item.lift()
        self.item.place(self.model.player.location)
        self.success = True
        self.message = message.Message(f"{0} drop[s] the {1}.",
                               noun1=self.actor.owner,
                               noun2=self.item)
        self.actor.reschedule(100)
        return self
