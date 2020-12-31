from __future__ import annotations
from typing import TYPE_CHECKING

from engine.events import Action, ActionWithItem, Impossible, message as message


class Equip(ActionWithItem):
    """Remove an item from inventory and place in an equipment slot."""

    def act(self) -> Action:
        components = self.model.player.components

        result = components['EQUIPMENT'].equip(self.item.slot, self.item)
        if not result:
            self.success = False
            self.message = message.Message(f"{0} cannot equip that!",
                                   noun1=self.actor.owner)
            raise Impossible(self)
        else:
            components['INVENTORY'].pop_item(self.item)
            self.success = True
            self.message = message.Message(f"{0} equip[s] the {1}",
                                   noun1=self.actor.owner,
                                   noun2=self.item)
            self.actor.reschedule(100)
            return self


class Dequip(ActionWithItem):
    """Remove an item from an equipment slot and place in inventory."""

    def act(self) -> Action:
        try:
            self.model.player.components['EQUIPMENT'].remove(self.item.slot)
            self.model.player.components['INVENTORY'].add_item(self.item)
            self.success = True
            self.message = message.Message(f"{0} remove[s] the {1} and stow[s] {1, message.THEM}.",
                                   noun1=self.actor.owner,
                                   noun2=self.item)
            self.actor.reschedule(100)
            return self
        except Impossible(self):
            self.success = False
            raise
