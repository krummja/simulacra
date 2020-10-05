from __future__ import annotations
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.components.actor import Actor
    from engine.area import Area
    from engine.location import Location
    from engine.model import Model
    from engine.items import Item


class Impossible(Exception):
    """Exception raised when an action cannot be performed."""


class Action:

    def __init__(self: Action, actor: Actor) -> None:
        self.actor = actor

    def plan(self: Action) -> Action:
        return self

    def act(self: Action) -> None:
        pass

    @property
    def location(self: Action) -> Location:
        return self.actor.location

    @property
    def area(self: Action) -> Area:
        return self.actor.location.area

    @property
    def model(self: Action) -> Model:
        return self.actor.location.area.model

    def report(self: Action, msg: str) -> None:
        return self.model.report(msg)


class ActionWithPosition(Action):

    def __init__(self, actor: Actor, position: Tuple[int, int]) -> None:
        super().__init__(actor)
        self.target_position = position


class ActionWithDirection(ActionWithPosition):

    def __init__(self, actor: Actor, direction: Tuple[int, int]) -> None:
        position = actor.location.x + direction[0], \
                   actor.location.y + direction[1]
        super().__init__(actor, position)
        self.direction = direction


class ActionWithItem(Action):

    def __init__(self, actor: Actor, target: Item):
        super().__init__(actor)
        self.item = target
