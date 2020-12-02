from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from config import DEBUG
from model import Model
from state import State, T, SaveAndQuit, GameOverQuit
from states.modal_state import ModalState
from storage import Storage
from views import MainMenuView
from generators.debug_map import debug_area

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

        #! START / NEW
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

        #! DELETE
        elif event.sym == tcod.event.K_d:
            if self.storage.save_slots[index] is not None:
                confirm_modal = ModalState(self.model, 'delete')
                #! Instead of having 'result' on the modal state, make the modal return bool
                #       result = confirm_modal.loop()
                #       if result: ...
                confirm_modal.loop()
                if confirm_modal.result:
                    self.storage.save_slots[index] = None
                else:
                    pass
            self.storage.write_to_file()

        #! QUIT
        elif event.sym == tcod.event.K_q:
            self.cmd_quit()

        #! NAVIGATE
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
