from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from actor import Actor
    from area import Area
    from location import Location
    from model import Model


class Impossible(Exception):
    """Exception raised when an action cannot be performed."""


class Action:

    def __init__(self, actor: Actor) -> None:
        self.actor = actor

    def plan(self) -> Action:
        return self

    def act(self) -> None:
        raise RuntimeError(f"{self.__class__.__name__} has no act implementation.")

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
