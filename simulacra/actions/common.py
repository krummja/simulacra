from __future__ import annotations

from rendering import update_fov
from geometry import *
from action import Action, Impossible
from result import Result
from action import (ActionWithPosition,
                    ActionWithItem,
                    ActionWithDirection)


class MoveToward(ActionWithPosition):
    """Move toward and possibly interact with a destination."""
    
    def plan(self) -> Action:
        
        dx = self.target_position[0] - self.location.x
        dy = self.target_position[1] - self.location.y
        distance = max(abs(dx), abs(dy))
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))
        return Move.Start(self.actor, (dx, dy)).plan()


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
            self.message = "it is too far."
            raise Impossible(self)
        
        if self.actor.owner.location.xy == self.target_position:
            self.success = True
            return self
        
        if self.area.is_blocked(*self.target_position):
            self.success = False
            self.effect = True
            self.message = "the way is blocked."
            raise Impossible(self)
        return self

    def act(self) -> Action:
        
        self.actor.owner.location = self.area[self.target_position]
        if self.actor.is_player:
            update_fov(self.area)
        self.actor.reschedule(100)
        self.success = True
        return self


class ActivateFromInventory(ActionWithItem):
    """Try to activate an item selected from an inventory."""
    pass


class ActivateNearby(ActionWithItem):
    """Try to activate a nearby object."""
    
    def plan(self) -> ActionWithItem:
        
        try:
            return self.item.plan_activate(self)
        except:
            self.success = False
            self.message = "nothing happens..."
            raise Impossible(self)

    def act(self) -> None:
        
        self.item.act_activate(self)


class Pickup(Action):
    """Remove an item from a nearby tile and place it in the player's
    inventory component.
    """
    
    def plan(self) -> Action:
        
        if not self.area.items.get(self.location.xy):
            self.success = False
            self.message = "there is nothing to pick up."
            raise Impossible(self)
        return self

    def act(self) -> Action:
        
        for item in self.area.items[self.location.xy]:
            try:
                self.success = True
                self.message = f"{self.actor.owner.noun_text} picks up the {item.noun_text}"
                item.lift()
                self.actor.owner.components['INVENTORY'].add_item(item)
                self.actor.reschedule(100)
                return self
            except:
                self.success = False
                self.message = f"cannot lift the {item.noun_text}!"
                raise Impossible(self)


class Drop(ActionWithItem):
    
    def act(self) -> Action:
        assert self.item in self.model.player.components['INVENTORY']['item_stacks'].keys()
        self.item.lift()
        self.item.place(self.model.player.location)
        self.success = True
        self.message = f"you drop the {self.item.noun_text}."
        self.actor.reschedule(100)
        return self


class Equip(ActionWithItem):
    
    def act(self) -> Action:
        components = self.model.player.components
        
        result = components['EQUIPMENT'].equip(self.item.slot, self.item)
        if not result:
            self.success = False
            self.message = "You cannot equip that!"
            raise Impossible(self)
        else:
            components['INVENTORY'].pop_item(self.item)
            self.success = True
            self.message = f"you equip the {self.item.noun_text}"
            self.actor.reschedule(100)
            return self


class Dequip(ActionWithItem):
    
    def act(self) -> Action:
        try:
            self.model.player.components['EQUIPMENT'].remove(self.item.slot)
            self.model.player.components['INVENTORY'].add_item(self.item)
            self.success = True
            self.message = f"you remove the {self.item.noun_text}"
            self.actor.reschedule(100)
            return self        
        except:
            self.success = False
            raise Impossible(self)
