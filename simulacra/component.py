from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class Component:
    """Components represent the interactive attributes of an entity.
    
    Every component should provide at least one option to present to any UI
    element that targets that component. For example, an Inventory component
    should provide a 'view' option that will appear in any menu raised as the
    result of an examine action.
    """

    NAME: str = '<unset>'

    def __init__(self):
        super().__init__()
        self.owner = None
        self.options = {}

    def on_register(self, owner: Entity) -> None:
        self.owner = owner

    def on_unregister(self) -> None:
        self.owner = None

    def update(self) -> None:
        pass

    def on_interact(self):
        pass