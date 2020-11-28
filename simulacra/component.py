from __future__ import annotations
from typing import Any, Dict, KeysView, ValuesView, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class Component:

    NAME = '<unset>'

    def __init__(self):
        super().__init__()
        self.owner = None

    def on_register(self, owner: Entity) -> None:
        self.owner = owner

    def on_unregister(self) -> None:
        self.owner = None

    def update(self) -> None:
        pass

    def handle_message(self, message):
        pass