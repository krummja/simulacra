from __future__ import annotations

from typing import Optional

from ..input.input_controller import T
from .state import State


class TestState(State):
    name: str = "TEST"

    def on_enter(self) -> None:
        self.manager.game.interface.transition(self.name)

    def cmd_confirm(self) -> Optional[T]:
        print("Command CONFIRM")

    def cmd_escape(self) -> None:
        self.cmd_quit()
