"""Common Actions"""

from __future__ import annotations

from engine.rendering import update_fov
from engine.events import (Action,
                           Impossible,
                           ActionWithPosition,
                           ActionWithItem,
                           ActionWithDirection)
import engine.events.message as message


class MoveToward(ActionWithPosition):
    """Move toward and possibly interact with a destination."""

    def plan(self) -> Action:
        dx = self.target_position[0] - self.location.x
        dy = self.target_position[1] - self.location.y
        distance = max(abs(dx), abs(dy))
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return MoveStart(self.actor, (dx, dy)).plan()


class MoveStart(ActionWithDirection):
    """Move an entity in a direction, interacting with obstacles."""

    def plan(self) -> ActionWithPosition:

        self.success = True
        return MoveEnd(self.actor, self.target_position).plan()


class MoveEnd(ActionWithPosition):
    """Move an entity to a destination, interacting with obstacles."""

    def plan(self) -> ActionWithPosition:

        if self.actor.owner.location.distance_to(*self.target_position) > 1:
            self.success = False
            self.message = message.Message("The distance is too great!")
            raise Impossible(self)

        if self.actor.owner.location.xy == self.target_position:
            self.success = True
            return self

        if self.area.is_blocked(*self.target_position):
            self.success = False
            self.effect = True
            self.message = message.Message("The way is blocked.")
            raise Impossible(self)
        return self

    def act(self) -> Action:

        self.actor.owner.location = self.area[self.target_position]
        if self.actor.is_player:
            update_fov(self.area)
        self.actor.reschedule(100)
        self.success = True
        return self


class ActivateFromInventory(ActionWithItem):
    """Try to activate an item selected from an inventory."""


class ActivateNearby(ActionWithItem):
    """Try to activate a nearby object."""

    def plan(self) -> ActionWithItem:
        try:
            return self.item.plan_activate(self)
        except Impossible(self):
            self.success = False
            self.message = message.Message("Nothing happens...")
            raise

    def act(self) -> None:
        self.item.act_activate(self)


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
