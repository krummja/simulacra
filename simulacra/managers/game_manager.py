from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

import manager
from managers.game_context import GameContext
from managers.console_manager import ConsoleManager
from managers.scene_manager import SceneManager


class GameManager(manager.BaseManager):
    
    def __init__(self) -> None:
        super().__init__()
        self.game_context = GameContext()
        self.console_manager = ConsoleManager()
        self.scene_manager = SceneManager()
    
    def start(self):
        pass
    
    def load_game(self):
        passs