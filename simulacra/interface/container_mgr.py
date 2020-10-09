from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.actions import ActionWithItem
    from engine.items import Item
    from engine.components.inventory import Inventory
    from engine.model import Model
    from states import State


class ContainerManager:
    """A mediator for handling actions that need to return access to an
    item's internal container inventory for interface rendering.
    """

    subscribers = []

    def add_subscriber(self: ContainerManager, state: State) -> None:
        self.subscribers.append(state)

    def notify(self: ContainerManager, action: ActionWithItem) -> None:
        for subscriber in self.subscribers:
            pass
