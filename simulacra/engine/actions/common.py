from __future__ import annotations

from engine.actions import (Impossible, Action, ActionWithPosition,
                            ActionWithDirection)


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
