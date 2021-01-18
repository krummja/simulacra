from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tcod.console import Console
    from .interface_manager import InterfaceManager


class View:
    name: str

    def __init__(self, manager: InterfaceManager) -> None:
        self.manager = manager

    def on_draw(self, console: Console) -> None:
        pass
