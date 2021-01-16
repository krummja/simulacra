from __future__ import annotations
from typing import TYPE_CHECKING

from engine.events import Action, ActionWithDirection, ActionWithPosition, \
    Impossible, message as message
from engine.rendering import update_fov


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
