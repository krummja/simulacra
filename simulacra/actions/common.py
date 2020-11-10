from __future__ import annotations

from rendering import update_fov
from action import Action, Impossible
from action import (ActionWithPosition,
                    ActionWithItem,
                    ActionWithDirection)


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
                # TODO: Make this more transparently hooked into the log
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
        pass


class Nearby(Action):

    class Examine(Action):
        pass

    class Pickup(Action):
        pass


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
