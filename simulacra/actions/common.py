from __future__ import annotations

from rendering import update_fov
from geometry import *
from action import Action, Impossible
from action import (ActionWithPosition,
                    ActionWithItem,
                    ActionWithDirection)

from data.animations import animations
from managers.manager_service import ManagerService

animation_manager = ManagerService().animation_manager


class Move(Action):

    class Toward(ActionWithPosition):
        """Move toward and possibly interact with a destination."""

        def plan(self) -> Action:
            dx = self.target_position[0] - self.location.x
            dy = self.target_position[1] - self.location.y
            distance = max(abs(dx), abs(dy))
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))
            return Move.Start(self.actor, (dx, dy)).plan()

    class Start(ActionWithDirection):
        """Move an entity in a direction, interacting with obstacles."""

        def plan(self) -> Action:
            return Move.End(self.actor, self.target_position).plan()

    class End(ActionWithPosition):
        """Move an entity to a destination, interacting with obstacles."""

        def plan(self) -> Action:
            if self.actor.owner.location.distance_to(*self.target_position) > 1:
                raise Impossible(
                    f"Cannot move from {self.actor.owner.location.xy} "
                    f"to {self.target_position}!"
                    )
            if self.actor.owner.location.xy == self.target_position:
                return self
            if self.area.is_blocked(*self.target_position):
                raise Impossible("the way is blocked.")
            return self

        def act(self) -> None:
            self.actor.owner.location = self.area[self.target_position]
            if self.actor.is_player:
                update_fov(self.area)
            self.actor.reschedule(100)


class Activate(Action):

    class FromInventory(ActionWithItem):
        pass

    class Nearby(ActionWithItem):
        def plan(self) -> ActionWithItem:
            try:
                return self.item.plan_activate(self)
            except Impossible("nothing happens..."):
                raise
            
        def act(self) -> None:
            self.item.act_activate(self)


class Nearby(Action):

    class Examine(Action):
        def plan(self) -> Action:
            for position in Point(*self.location.xy).neighbors:
                try:
                    if self.area.items[position[0], position[1]]:
                        self.area.nearby_items.append(self.area.items[position])
                except KeyError:
                    continue
            return self
                
        def act(self) -> None:
            if len(self.area.nearby_items) > 0:
                for items in self.area.nearby_items:
                    for item in items:
                        self.model.report(f"{item} is nearby.")
                self.area.nearby_items.clear()
            else:
                self.model.report("there is nothing of note nearby")
            self.actor.reschedule(100)

    class Pickup(Action):
        def plan(self) -> Action:
            if not self.area.items.get(self.location.xy):
                raise Impossible("there is nothing to pick up.")
            return self
        
        def act(self) -> None:
            for item in self.area.items[self.location.xy]:
                try:
                    self.report(f"{self.actor.owner.noun_text} picks up the {item.noun_text}.")
                    self.actor.owner.components['INVENTORY'].take(item)
                    return self.actor.reschedule(100)
                except Impossible:
                    self.report(f"{self.actor.owner.noun_text} cannot lift the {item.noun_text}!")


class Attack(Action):

    class Player(Action):
        pass

    class Hostile(Action):
        pass

    class Friendly(Action):
        pass

    class WithAbility(Action):
        pass

    class WithItem(Action):
        pass

    class WithMagic(Action):
        pass
