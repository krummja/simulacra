from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from config import DEBUG
from model import Model
from state import State, T, SaveAndQuit, GameOverQuit
from states.modal_states.confirm_modal_state import ConfirmModalState
from storage import Storage
from views import MainMenuView
from generators.debug_map import debug_area
from generators.testing_map import testing_area

if TYPE_CHECKING:
    from managers.manager_service import ManagerService
    from factories.factory_service import FactoryService


class MainMenuState(State[None]):

    NAME = "Main Menu"

    def __init__(self) -> None:
        super().__init__()
        self._storage: Storage = Storage()
        self._storage.load_from_file()
        self._view = MainMenuView(self)

    @property
    def storage(self):
        return self._storage

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:
        index = self._view.character_select.index_as_int

        if event.sym == tcod.event.K_RETURN:
            menu_data = self.storage.save_slots[index]
            if menu_data is not None:
                if DEBUG:
                    print("Storage: Save data found")
                self._model = self.storage.save_slots[index]
                self.manager_service.initialize_managers(self._model)
                self.start()
            else:
                if DEBUG:
                    print("Storage: No data for this slot.")
                self.new_game()

        elif event.sym == tcod.event.K_d:
            if self.storage.save_slots[index] is not None:
                confirm_modal = ConfirmModalState(self.model)
                confirm_modal.loop()
                if confirm_modal.result:
                    self.storage.save_slots[index] = None
                else:
                    pass
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
            self.manager_service.initialize_managers(self._model)
            
            # TODO: Build an area manager to handle injecting areas easier
            # self._model.area_data.current_area = testing_area(self._model)
            self._model.area_data.current_area = debug_area(self._model)
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
