"""ENGINE.COMPONENTS.Component

Base Component class.
"""
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.entities.entity import Entity


class Component(defaultdict):
    """Components represent the interactive attributes of an entity.

    Every component should provide at least one option to present to any UI
    element that targets that component. For example, an Inventory component
    should provide a 'view' option that will appear in any menu raised as the
    result of an examine action.
    """

    def __init__(self, uid: str = "<unset>") -> None:
        super().__init__()
        self.uid = uid
        self.owner: Entity = None

    def on_register(self, owner: Entity) -> None:
        self.owner = owner

    def on_unregister(self) -> None:
        self.owner = None
