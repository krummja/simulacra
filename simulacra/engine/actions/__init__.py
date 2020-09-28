from __future__ import annotations  # type: ignore
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from engine.actor import Actor
    from engine.area import Area
    from engine.items import Item
    from engine.location import Location
    from engine.model import Model


class Impossible(Exception):
    """Exception raised when an action cannot be performed.
    
    Includes the reason as the exception message.
    """


class Action:

    def __init__(self, actor: Actor) -> None:
        self.actor = actor

    def plan(self) -> Action:
        """Return the action to perform.
        
        This method can be overridden by specific `Action` types to control
        the conditions on which it will successfully be returned.
        """
        return self

    def act(self) -> None:
        """Execute the action for this class.

        This method must be implemented separately. If the `plan()` method
        return successfully, this method will run next which activates the
        actual behavior.
        """
        raise RuntimeError(f"{self.__class__} has no act implementation.")

    @property
    def location(self) -> Location:
        return self.actor.location

    @property
    def area(self) -> Area:
        return self.actor.location.area

    @property
    def model(self) -> Model:
        return self.actor.location.area.model

    def report(self, msg: str) -> None:
        return self.model.report(msg)


class ActionWithPosition(Action):

    def __init__(self, actor: Actor, position: Tuple[int, int]) -> None:
        super().__init__(actor)
        self.target_pos = position


class ActionWithDirection(ActionWithPosition):
    
    def __init__(self, actor: Actor, direction: Tuple[int, int]) -> None:
        position = actor.location.x + direction[0], actor.location.y + direction[1]
        super().__init__(actor, position)
        self.direction = direction


class ActionWithEntity(Action):

    def __init__(self, actor: Actor, target: Actor) -> None:
        super().__init__(actor)
        self.target = target


class ActionWithItem(Action):
    """A relation between some `Actor` and some `Item`.

    For example, a `Player` `Actor` might wish to use a `Potion`, which would
    entail that actor=player and target=potion. A specific action like 
    `action.item.consume()` would then call the relevant `consume()` method on
    the target item.
    """

    def __init__(self, actor: Actor, target: Item) -> None:
        super().__init__(actor)
        self.item = target