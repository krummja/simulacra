import tcod
import time
import numpy as np

import config
from states.main_menu_state import MainMenuState
from tilemap import tileset

def main() -> None:
    
    with tcod.context.new_terminal(
            columns=config.CONSOLE_WIDTH,
            rows=config.CONSOLE_HEIGHT,
            tileset=tileset,
            title="Simulacra",
            vsync=True
        ) as config.CONTEXT:
        while True:
            MainMenuState().loop()


if __name__ == '__main__':
    main()