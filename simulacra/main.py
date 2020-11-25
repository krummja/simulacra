from __future__ import annotations

import tcod
import config
from states.main_menu_state import MainMenuState
from factories.factory_service import FactoryService
from managers.manager_service import ManagerService


def main() -> None:
    with tcod.context.new_terminal(
            columns=config.CONSOLE_WIDTH,
            rows=config.CONSOLE_HEIGHT,
            tileset=config.TILESET,
            title="Simulacra",
            vsync=True
        ) as config.CONTEXT:
        while True:
            factory_service = FactoryService()
            manager_service = ManagerService()
            manager_service.animation_manager.start()
            manager_service.animation_manager.loop()
            MainMenuState(manager_service, factory_service).loop()


if __name__ == '__main__':
    main()
