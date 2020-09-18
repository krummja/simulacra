import tcod
from tcod.tileset import Tileset


TILE_SCALE: int = 16
TILESET: Tileset = tcod.tileset.load_truetype_font("./simulacra/assets/simulacra.ttf", TILE_SCALE, TILE_SCALE)

CONSOLE_WIDTH: int = 110
CONSOLE_HEIGHT: int = 55

STAGE_WIDTH: int = 256
STAGE_HEIGHT: int = 256

STAGE_PANEL_WIDTH: int = (CONSOLE_WIDTH // 4) * 3
STAGE_PANEL_HEIGHT: int = CONSOLE_HEIGHT

SIDE_PANEL_WIDTH: int = CONSOLE_WIDTH - STAGE_PANEL_WIDTH
SIDE_PANEL_HEIGHT: int = CONSOLE_HEIGHT