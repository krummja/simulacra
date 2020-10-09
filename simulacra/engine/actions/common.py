from __future__ import annotations

from engine.items.door import Door
from engine.geometry import *
from engine.actions import (Impossible, Action, ActionWithPosition,
                            ActionWithDirection, ActionWithItem)


class Wait(Action):

    def act(self: Wait) -> None:
        if self.actor.is_player:
            self.area.update_fov()
        self.actor.reschedule(0)


class MoveStart(ActionWithPosition):

    def plan(self: MoveStart) -> Action:
        if self.actor.location.distance_to(*self.target_position) > 1:
            raise Impossible(
                f"can't move from {self.actor.location.xy} "
                f"to {self.target_position}."
                )
        if self.actor.location.xy == self.target_position:
            return self
        if self.area.is_blocked(*self.target_position):
            try:
                if self.area.items[self.target_position]:
                    for item in self.area.items[self.target_position]:
                        if isinstance(item, Door) and item.is_locked is False:
                            ActivateNearby(self.actor, item).plan().act()
            except KeyError:
                raise Impossible("the way is blocked.")
        return self

    def act(self: MoveStart) -> None:
        self.actor.owner.location = self.area[self.target_position]
        if self.actor.is_player:
            self.area.update_fov()
        self.actor.reschedule(100)


class Move(ActionWithDirection):

    def plan(self: Move) -> Action:
        return MoveStart(self.actor, self.target_position).plan()


class MoveEnd(ActionWithPosition):

    def plan(self: MoveEnd) -> Action:
        dx = self.target_position[0] - self.location.x
        dy = self.target_position[1] - self.location.y
        distance = max(abs(dx), abs(dy))
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return Move(self.actor, (dx, dy)).plan()


class ExamineNearby(Action):

    def plan(self: ExamineNearby) -> Action:
        for position in Point(*self.location.xy).neighbors:
            try:
                if self.area.items[position[0], position[1]]:
                    self.area.nearby_items.append(self.area.items[position])
            except KeyError:
                continue
        return self

    def act(self: ExamineNearby) -> None:
        if len(self.area.nearby_items) > 0:
            for items in self.area.nearby_items:
                for item in items:
                    # TODO: Use the noun_text attribute
                    # TODO: Set up a way to parse a/an prefixing
                    self.model.report(f"{item} is nearby.")
            self.area.nearby_items.clear()
        else:
            self.model.report("There is nothing of note nearby.")


class ActivateItem(ActionWithItem):

    def plan(self: ActivateItem) -> ActionWithItem:
        assert self.item in self.actor.owner.components['INVENTORY'].contents
        return self.item.plan_activate(self)

    def act(self: ActivateItem) -> None:
        assert self.item in self.actor.owner.components['INVENTORY'].contents
        self.item.action_activate(self)
        self.actor.reschedule(100)


class ActivateNearby(ActionWithItem):

    def plan(self: ActivateNearby) -> ActionWithItem:
        if self.item.interactive:
            try:
                return self.item.plan_activate(self)
            except Impossible("nothing happens..."):
                raise
        else:
            raise Impossible("nothing happens...")

    def act(self: ActivateNearby) -> None:
        self.item.action_activate(self)
        self.actor.reschedule(100)


class Pickup(Action):

    def plan(self: Pickup) -> Action:
        if not self.area.items.get(self.location.xy):
            raise Impossible("there is nothing to pick up.")
        return self

    def act(self: Pickup) -> None:
        for item in self.area.items[self.location.xy]:
            try:
                if item.components['PHYSICS'].movable:
                    self.report(f"{self.actor.owner.noun_text} picks up the {item.noun_text}.")
                    self.actor.owner.components['INVENTORY'].take(item)
                    return self.actor.reschedule(100)
                else:
                    raise Impossible(f"the {item.noun_text} doesn't budge...")
            except Impossible:
                self.report(f"{self.actor.owner.noun_text} cannot lift the {item.noun_text}!")


class Attack(ActionWithPosition):
    pass


class AttackPlayer(Action):
    pass


class DropItem(ActionWithItem):
    pass


class DrinkItem(ActionWithItem):
    pass

