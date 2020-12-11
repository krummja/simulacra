from __future__ import annotations
from typing import Dict, TYPE_CHECKING
import tcod

if TYPE_CHECKING:
    from tcod.console import Console
    from tcod.tileset import Tileset

CONTEXT: tcod.context.Context

CONSOLE_WIDTH: int = 110
CONSOLE_HEIGHT: int = 55

STAGE_WIDTH: int = 256
STAGE_HEIGHT: int = 256

STAGE_PANEL_WIDTH: int = (CONSOLE_WIDTH // 3) * 2
STAGE_PANEL_HEIGHT: int = (CONSOLE_HEIGHT // 4) * 3

SIDE_PANEL_WIDTH: int = CONSOLE_WIDTH - STAGE_PANEL_WIDTH
SIDE_PANEL_HEIGHT: int = CONSOLE_HEIGHT

TILESET: Tileset = tcod.tileset.load_truetype_font(
    "./assets/simulacra.ttf", 16, 16
    # "simulacra/assets/simulacra.ttf", 16, 16
    )

CONSOLES: Dict[str, Console] = {
    'INTERFACE': tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT),
    'EFFECTS': tcod.Console(CONSOLE_WIDTH, CONSOLE_HEIGHT),
    'ROOT': tcod.Console(width=CONSOLE_WIDTH, height=CONSOLE_HEIGHT)
    }

DEBUG = False
ADMIN = True