"""ENGINE.EVENTS.Action

Define basic actions for use with the `EventQueue`.

Classes:

    Action
    ActionWithPosition(Action)
    ActionWithDirection(ActionWithPosition)
    ActionWithItem(Action)
    Impossible(Exception)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

from .result import Result

if TYPE_CHECKING:
    from actor import Actor
    from engine.areas import Area, Location
    from engine.entities import Item
    from engine.model import Model


class Impossible(Exception):
    """Exception raised when an action cannot be performed."""


class Action:
    """Base `Action` object.

    Defines an action to be performed by an `Actor`.
    Provides basic properties for handling `Result` objects and reporting
    to the game's log.
    """

    def __init__(self, actor: Actor) -> None:
        """Constructor.

        Args:
            actor (Actor): The `Actor` executing this `Action`.
        """
        self.actor = actor
        self.done = False
        self.success = False
        self.effect = None
        self.message = ""

    def plan(self) -> Action:
        """Check(s) to perform prior to executing `Action.act()`.

        This method may be overridden to run checks prior to the execution
        of the actual effect of the action.

        For example, if an `Action` would interact with another game object,
        such as picking something up, the relevant planning step might be to
        check that an item actually exists, that it is able to be picked up,
        that it is not harmful, etc.

        Returns:
            Action: The instigating `Action`.
        """
        return self

    def act(self) -> Optional[Result]:
        """Method for executing the `Action`."""
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

    def make_result(self, action: Action) -> Result:
        result = Result(
            actor=action.actor,
            event=action,
            success=action.success,
            effect=action.effect,
            message=action.message
            )
        return result

    def report(self, msg: str) -> None:
        message = self.model.report(msg)
        return message


class ActionWithPosition(Action):
    """Base class for `Action` instances that require a position argument."""

    def __init__(self, actor: Actor, position: Tuple[int, int]) -> None:
        super().__init__(actor)
        self.target_position = position


class ActionWithDirection(ActionWithPosition):
    """Base class for `Action` instances which require a direction argument."""

    def __init__(self, actor: Actor, direction: Tuple[int, int]) -> None:
        position = (actor.location.x + direction[0],
                    actor.location.y + direction[1])
        super().__init__(actor, position)
        self.direction = direction


class ActionWithItem(Action):
    """Base class for `Action` instances which interface with an `Item`."""

    def __init__(self, actor: Actor, target: Item) -> None:
        super().__init__(actor)
        self.item = target
