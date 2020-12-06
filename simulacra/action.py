from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

from config import DEBUG

if TYPE_CHECKING:
    from actor import Actor
    from area import Area
    from location import Location
    from model import Model
    from item import Item


class Impossible(Exception):
    """Exception raised when an action cannot be performed."""


class Action:

    def __init__(self, actor: Actor) -> None:
        self.actor = actor

    def plan(self) -> Action:
        return self

    def act(self) -> None:
        raise RuntimeError(f"{self.__class__.__name__} "
                            "has no act implementation.")

    @property
    def area(self) -> Area:
        return self.actor.location.area

    @property
    def location(self) -> Location:
        return self.actor.location

    @property
    def model(self) -> Model:
        return self.actor.location.area.model

    def report(self, msg: str) -> None:
        return self.model.report(msg)


class ActionWithPosition(Action):

    def __init__(self, actor: Actor, position: Tuple[int, int]) -> None:
        super().__init__(actor)
        self.target_position = position


class ActionWithDirection(ActionWithPosition):

    def __init__(self, actor: Actor, direction: Tuple[int, int]) -> None:
        position = (actor.location.x + direction[0], 
                    actor.location.y + direction[1])
        super().__init__(actor, position)
        self.direction = direction
        
        #! DEBUG ///////////////////////////////////////////////////////////////////////////////////////////////////////
        #! Prints the start position, move direction, and end position of every ActionWithDirection instance.
        if DEBUG:
            print(f"ActionWithDirection  > position:  {actor.location.x, actor.location.y}")
            print(f"ActionWithDirection  > direction: {direction}")
            print(f"ActionWithPosition   > position:  {position}")
            print("----------------------------------------------------")
        #! /////////////////////////////////////////////////////////////////////////////////////////////////////////////
        

class ActionWithItem(Action):

    def __init__(self, actor: Actor, target: Item) -> None:
        super().__init__(actor)
        self.item = target
