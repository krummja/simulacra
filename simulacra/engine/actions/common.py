from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.actions import (
    Impossible,
    Action,
    ActionWithPosition,
    ActionWithDirection,
    ActionWithItem
)
from engine.items.other import Door


class MoveTo(ActionWithPosition):

    def plan(self) -> Action:
        if self.actor.location.distance_to(*self.target_pos) > 1:
            raise Impossible(
                f"Can't move from {self.actor.location.xy} to {self.target_pos}."
            )
        if self.actor.location.xy == self.target_pos:
            return self
        if self.area.combatant_at(*self.target_pos):
            return Attack(self.actor, self.target_pos).plan()
        if self.area.interactable_at(*self.target_pos):
            return Interact(self.actor, self.target_pos).plan()
        if self.area.is_blocked(*self.target_pos):
            raise Impossible("The way is blocked.")
        return self

    def act(self) -> None:
        self.actor.location = self.area[self.target_pos]
        
        if self.actor.is_player():
            self.area.update_fov()
        self.actor.reschedule(100)


class Interact(ActionWithPosition):
    
    def plan(self) -> Interact:
        for item in self.area.items[self.target_pos]:
            if item.is_interactable:
                return item.plan_activate(self)
        return self


class Move(ActionWithDirection):

    def plan(self) -> Action:
        return MoveTo(self.actor, self.target_pos).plan()


class MoveTowards(ActionWithPosition):

    def plan(self) -> Action:
        dx = self.target_pos[0] - self.location.x
        dy = self.target_pos[1] - self.location.y
        distance = max(abs(dx), abs(dy))
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return Move(self.actor, (dx, dy)).plan()


class Open(ActionWithItem):

    def act(self) -> None:
        self.item.open()
        self.actor.reschedule(100)


class Attack(ActionWithPosition):

    def plan(self) -> Attack:
        if self.location.distance_to(*self.target_pos) > 1:
            raise Impossible("That space is too far away to attack.")
        return self

    def act(self) -> None:
        target = self.area.combatant_at(*self.target_pos)
        assert target

        attacker_name = self.actor.character.name
        target_name = target.character.name

        attack = self.actor.character.attributes['might'].current_value
        against = target.character.attributes['resilience'].current_value

        damage = attack - against

        if self.actor.is_player():
            who_desc = f"You attack the {target_name}"
        else:
            who_desc = f"{attacker_name} attacks {target_name}"
        
        if damage > 0:
            self.report(f"{who_desc} for {damage}!")
            target.damage(damage)
        else:
            self.report(f"{who_desc} but does no damage.")
        self.actor.reschedule(100)


class AttackPlayer(Action):

    def plan(self) -> Action:
        return MoveTowards(self.actor, self.area.player.location.xy).plan()
