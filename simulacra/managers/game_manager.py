from __future__ import annotations
import typing

import tcod
from .console_manager import ConsoleManager


class GameManager:
    
    def __init__(self) -> None:
        self.console_manager = ConsoleManager(self)
        self.root_console = self.console_manager.root_console
        
        self.state_manager = None
        self.result_manager = None
        self.action_manager = None
        
    def loop(self) -> None:
        while True:
            self.console_manager.context.present(self.root_console)