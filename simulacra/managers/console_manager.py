from __future__ import annotations
from typing import TYPE_CHECKING

import tcod
from config import *

if TYPE_CHECKING:
    from tcod.console import Console


class ConsoleManager:
    
    def __init__(self) -> None:
        self.main_console: Console = None
    
    def render_console(self, console: Console, pos_x: int, pos_y: int) -> None:
        console.blit(self.main_console, pos_x, pos_y, pos_x, pos_y)
    
    def clear(self) -> None:
        self.main_console.clear()
        
    @staticmethod
    def create_new_console(width: int, height: int) -> Console:
        return tcod.Console(width, height)