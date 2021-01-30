from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..input.input_controller import T
from .screen import Screen

if TYPE_CHECKING:
    from .screen_manager import ScreenManager
    from simulacra.core.game import Game


class MainMenuScreen(Screen):
    name: str = "MAIN MENU"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self.game: Game = manager.game

    def on_enter(self) -> None:
        print("Entered Main Menu")

    def on_leave(self) -> None:
        print("Leaving Main Menu")

    def on_update(self, dt) -> None:
        self.handle_input()

    def cmd_move(self, x: int, y: int) -> Optional[T]:
        pass

    def cmd_confirm(self) -> Optional[T]:
        self.manager.push_screen('STAGE')

    def cmd_escape(self) -> None:
        self.cmd_quit()
