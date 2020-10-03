from __future__ import annotations
from typing import List, TYPE_CHECKING

from engine.geometry import *
from engine.actions import (Impossible, Action, ActionWithPosition,
                            ActionWithDirection)

if TYPE_CHECKING:
    from engine.items import Item


class MoveTo(ActionWithPosition):

    def plan(self: MoveTo) -> Action:
        if self.actor.location.distance_to(*self.target_position) > 1:
            raise Impossible(
                f"Can't move from {self.actor.location.xy} "
                f"to {self.target_position}."
                )
        if self.actor.location.xy == self.target_position:
            return self
        if self.area.is_blocked(*self.target_position):
            raise Impossible("The way is blocked.")
        return self

    def act(self: MoveTo) -> None:
        self.actor.location = self.area[self.target_position]
        if self.actor.is_player():
            self.area.update_fov()
        self.actor.reschedule(100)


class MoveTowards(ActionWithPosition):

    def plan(self: MoveTowards) -> Action:
        dx = self.target_position[0] - self.location.x
        dy = self.target_position[1] - self.location.y
        distance = max(abs(dx), abs(dy))
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return Move(self.actor, (dx, dy)).plan()


class Move(ActionWithDirection):

    def plan(self: Move) -> Action:
        return MoveTo(self.actor, self.target_position).plan()


class ExamineNearby(Action):

    items = []

    def plan(self: ExamineNearby) -> Action:
        for position in Point(*self.location.xy).neighbors:
            try:
                if self.area.items[position[0], position[1]]:
                    self.items.append(self.area.items[position])
            except KeyError:
                continue
        return self

    def act(self: ExamineNearby) -> None:
        if len(self.items) > 0:
            for items in self.items:
                for item in items:
                    self.model.report(f"You see {item.noun_text} nearby.")
            self.items.clear()
        else:
            self.model.report("There is nothing of note nearby.")
