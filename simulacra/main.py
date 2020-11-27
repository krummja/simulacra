import tcod

import config
from managers.manager_service import ManagerService
from factories.factory_service import FactoryService
from states.main_menu_state import MainMenuState

manager_service = ManagerService()
factory_service = FactoryService()


def main() -> None:
    
    with tcod.context.new_terminal(
            columns=config.CONSOLE_WIDTH,
            rows=config.CONSOLE_HEIGHT,
            tileset=config.TILESET,
            title="Simulacra",
            vsync=True
        ) as config.CONTEXT:
        while True:
            MainMenuState().loop()


if __name__ == '__main__':
    main()