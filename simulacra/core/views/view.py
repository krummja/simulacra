from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tcod.console import Console
    from .interface_manager import InterfaceManager


class View:
    """The largest organizational unit for on-screen UI elements.

    A View is one or more UI elements that display information to the player.
    The data presented is typically contextualized to a single game state.
    """

    name: str

    def __init__(self, manager: InterfaceManager) -> None:
        self.manager = manager

    def on_draw(self, console: Console) -> None:
        pass
