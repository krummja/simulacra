from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .screen_manager import ScreenManager
    from simulacra.core.game import Game


class Screen:
    name: str

    def __init__(self, manager: ScreenManager) -> None:
        self.manager = manager
        self._game: Game = manager.game

    def on_enter(self):
        pass

    def on_leave(self):
        pass

    def on_update(self, dt):
        pass
