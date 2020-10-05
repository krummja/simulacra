from __future__ import annotations

from engine.geometry import *
from engine.actions import (Impossible, Action, ActionWithPosition,
                            ActionWithDirection, ActionWithItem)
from engine.items.door import Door


class Wait(Action):

    def act(self: Wait) -> None:
        self.actor.location = self.actor.location
        if self.actor.is_player:
            self.area.update_fov()
        self.actor.reschedule(100)


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
        if self.actor.is_player:
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

    def plan(self: ExamineNearby) -> Action:
        for position in Point(*self.location.xy).neighbors:
            try:
                if self.area.items[position[0], position[1]]:
                    self.area.nearby_items.append(self.area.items[position])
                    print(self.area.nearby_items)
            except KeyError:
                continue
        return self

    def act(self: ExamineNearby) -> None:
        if len(self.area.nearby_items) > 0:
            for items in self.area.nearby_items:
                for item in items:
                    self.model.report(f"You see {item} nearby.")
            self.area.nearby_items.clear()
        else:
            self.model.report("There is nothing of note nearby.")


class ActivateItem(ActionWithItem):

    def plan(self: ActivateItem) -> ActionWithItem:
        # TODO: Hmm... this is a bit of a messy situation
        assert self.item in self.actor.game_object.components['INVENTORY'].contents
        return self.item.plan_activate(self)

    def act(self: ActivateItem) -> None:
        assert self.item in self.actor.game_object.components['INVENTORY'].contents
        self.item.action_activate(self)
        self.actor.reschedule(100)


class ActivateNearby(ActionWithItem):

    def plan(self: ActivateNearby) -> ActionWithItem:
        # TODO: Replace with a check against "item.interactive"
        assert isinstance(self.item, Door)
        return self.item.plan_activate(self)

    def act(self: ActivateNearby) -> None:
        assert isinstance(self.item, Door)
        self.item.mut_state()
        self.actor.reschedule(100)


class Pickup(Action):

    # FIXME: Clean up the pickup logic, notably it reports item is picked up even when it cannot be
    def plan(self: Pickup) -> Action:
        if not self.area.items.get(self.location.xy):
            raise Impossible("There is nothing to pick up.")
        return self

    def act(self: Pickup) -> None:
        for item in self.area.items[self.location.xy]:
            self.report(f"{self.actor.game_object.noun_text} picks up the {item.noun_text}")
            self.actor.game_object.components['inventory'].take(item)
            return self.actor.reschedule(100)
