from __future__ import annotations
from typing import Dict, TYPE_CHECKING
from pathlib import Path
import tcod

if TYPE_CHECKING:
    from tcod.console import Console

CONTEXT: tcod.context.Context

CONSOLE_WIDTH: int = 110
CONSOLE_HEIGHT: int = 55

STAGE_WIDTH: int = 256
STAGE_HEIGHT: int = 256

STAGE_PANEL_WIDTH: int = (CONSOLE_WIDTH // 3) * 2
STAGE_PANEL_HEIGHT: int = (CONSOLE_HEIGHT // 4) * 3

SIDE_PANEL_WIDTH: int = CONSOLE_WIDTH - STAGE_PANEL_WIDTH
SIDE_PANEL_HEIGHT: int = CONSOLE_HEIGHT
        
CONSOLES: Dict[str, Console] = {
    'INTERFACE': tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT),
    'EFFECTS': tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT),
    'ROOT': tcod.Console(width=CONSOLE_WIDTH, height=CONSOLE_HEIGHT)
    }

DEBUG = False
ADMIN = True