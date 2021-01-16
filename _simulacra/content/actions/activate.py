from __future__ import annotations
from typing import TYPE_CHECKING

from engine.events import ActionWithItem, Impossible, message as message


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
