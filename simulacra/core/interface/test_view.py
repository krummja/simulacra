from __future__ import annotations
from typing import TYPE_CHECKING

from .view import View

if TYPE_CHECKING:
    from tcod.console import Console
    from .interface_manager import InterfaceManager


class TestView(View):
    name: str = "TEST"

    def __init__(self, manager: InterfaceManager) -> None:
        self.manager = manager

    def on_draw(self, console: Console) -> None:
        console.print(2, 2, "TestView says: Hello, world!")
