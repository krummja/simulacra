from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from ..input.input_controller import T
from .screen import Screen

if TYPE_CHECKING:
    from .screen_manager import ScreenManager
    from simulacra.core.game import Game


class TestScreen(Screen):
    name: str = "TEST"

    def __init__(self, manager: ScreenManager) -> None:
        super().__init__(manager)
        self._game: Game = manager.game

    def on_enter(self) -> None:
        print(f"Entered: {self.name}")

    def handle_input(self):
        command = self._game.input.handle_input()
        if not command:
            return
        command()

    def on_update(self, dt) -> None:
        self.handle_input()
        self._game.update_engine_systems(dt)

    def cmd_confirm(self) -> Optional[T]:
        print("Command CONFIRM")

    def cmd_escape(self) -> None:
        self.cmd_quit()
