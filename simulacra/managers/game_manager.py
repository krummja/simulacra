from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
import config

from game_context import GameContext
from managers.manager_service import ManagerService
from managers.animation_manager import AnimationManager
from managers.interface_manager import InterfaceManager
from managers.state_manager import StateManager
from managers.console_manager import ConsoleManager


class GameManager:
    
    def __init__(self) -> None:
        self.console_manager = ConsoleManager()
        self.game_context = GameContext()
        self.state_manager = StateManager(self.console_manager, 
                                          self.game_context)
        
    def start(self) -> None:
        self.state_manager.transition_to("MainMenu")
        with tcod.context.new_terminal(
                columns=config.CONSOLE_WIDTH,
                rows=config.CONSOLE_HEIGHT,
                tileset=config.TILESET,
                title="Simulacra",
                vsync=True
            ) as config.CONTEXT:
            while True:
                self.state_manager.current_state.loop()