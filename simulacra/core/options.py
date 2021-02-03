CONSOLE_WIDTH: int = 192
CONSOLE_HEIGHT: int = 56

STAGE_SIZE: int = 32
STAGE_WIDTH: int = STAGE_SIZE
STAGE_HEIGHT: int = STAGE_SIZE

SCALE: int = 2
TILE_SIZE: int = 16
HALF_TILE_SIZE: int = TILE_SIZE // 2

DEFAULT_TILESET: str = "Simulacra"
TILE_ALIGN: str = "top-left"
CODEPAGE: str = "1250"
RESIZE_FILTER: str = "nearest"
SPACING: str = "2x1"

FULLSCREEN: bool = True

STAGE_PANEL_WIDTH: int = 128
STAGE_PANEL_HEIGHT = CONSOLE_HEIGHT

SIDE_PANEL_WIDTH: int = CONSOLE_WIDTH - STAGE_PANEL_WIDTH
SIDE_PANEL_HEIGHT: int = CONSOLE_HEIGHT

LOG_PANEL_HEIGHT: int = (CONSOLE_HEIGHT // 4)

DEBUG: bool = False
DEVELOP: bool = True
VIEW_RADIUS: int = 10 if DEBUG is False else 30
