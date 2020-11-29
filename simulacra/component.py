from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

from util import Data

if TYPE_CHECKING:
    from entity import Entity


class Component(Data):
    """Components represent the interactive attributes of an entity.
    
    Every component should provide at least one option to present to any UI
    element that targets that component. For example, an Inventory component
    should provide a 'view' option that will appear in any menu raised as the
    result of an examine action.
    """

    NAME: str = '<unset>'

    def __init__(self, **kwargs):
        super().__init__(self.NAME)
        self.owner = None

    def on_register(self, owner: Entity) -> None:
        self.owner = owner

    def on_unregister(self) -> None:
        self.owner = None
