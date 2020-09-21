from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.actions import (
    Impossible,
    Action,
    ActionWithPosition,
    ActionWithDirection,
    ActionWithItem
)


class MoveTo(ActionWithPosition):

    def plan(self) -> Action:
        if self.actor.location.distance_to(*self.target_pos) > 1:
            raise Impossible(
                f"Can't move from {self.actor.location.xy} to {self.target_pos}."
            )
        if self.actor.location.xy == self.target_pos:
            return self
        if self.area.is_blocked(*self.target_pos):
            raise Impossible("The way is blocked.")
        return self

    def act(self) -> None:
        # This is very cool - the `getitem` magic method in Area allows this!
        self.actor.location = self.area[self.target_pos]
        
        if self.actor.is_player():
            self.area.update_fov()
        self.actor.reschedule(100)

class Move(ActionWithDirection):

    def plan(self) -> Action:
        return MoveTo(self.actor, self.target_pos).plan()