from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

from collections import defaultdict

if TYPE_CHECKING:
    from entity import Entity


class Component(defaultdict):
    """Components represent the interactive attributes of an entity.
    
    Every component should provide at least one option to present to any UI
    element that targets that component. For example, an Inventory component
    should provide a 'view' option that will appear in any menu raised as the
    result of an examine action.
    """

    NAME: str = '<unset>'
    OWNER: Entity = None

    def __init__(self, name: str):
        self.NAME = name

    def on_register(self, owner: Entity) -> None:
        self.OWNER = owner

    def on_unregister(self) -> None:
        self.OWNER = None
