from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from model import Model
from state import State, T, SaveAndQuit, GameOverQuit
from storage import Storage
from views import MainMenuView
from generators.debug_map import debug_area

if TYPE_CHECKING:
    from managers.manager_service import ManagerService
    from factories.factory_service import FactoryService
    from managers.game_context import GameContext


class MainMenuState(State[None]):

    def __init__(
            self,
            manager_service: ManagerService,
            factory_service: FactoryService
        ) -> None:
        super().__init__(manager_service, factory_service)
        self._model: Optional[Model] = None
        self._view = MainMenuView(self)
        self._storage: Storage = Storage()
        self._storage.load_from_file()

    @property
    def storage(self):
        return self._storage

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        index = self._view.character_select.index_as_int

        if event.sym == tcod.event.K_RETURN:
            menu_data = self.storage.save_slots[index]
            if menu_data is not None:
                print("Storage: Save data found")
                self._model = self.storage.save_slots[index]
                self.start()
            else:
                print("Storage: No data for this slot.")
                self.new_game()

        elif event.sym == tcod.event.K_d:
            if self.storage.save_slots[index] is not None:
                self.storage.save_slots[index] = None
            self.storage.write_to_file()

        elif event.sym == tcod.event.K_q:
            self.cmd_quit()

        elif event.sym in self.MOVE_KEYS:
            self._view.character_select.current_index = (
                self.MOVE_KEYS[event.sym][0],
                self.MOVE_KEYS[event.sym][1]
                )

        return super().ev_keydown(event)

    def new_game(self) -> None:
        try:
            self._model = Model()
            self._context.start_service(self._model)
            self._model.area_data.current_area = debug_area(
                self._model,
                self.manager_service,
                self.factory_service
                )
            self.storage.add_save(self._view.character_select.index_as_int,
                                  self.model)
            self.start()
        except SystemExit:
            raise

    def start(self) -> None:
        assert self.model
        try:
            self.model.loop()
        except SaveAndQuit:
            self.storage.write_to_file()
        except SystemExit:
            self.storage.write_to_file()
