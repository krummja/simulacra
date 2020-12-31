"""ENGINE.STATES.Main_Menu_State"""
from __future__ import annotations

from typing import Optional

import tcod

from config import DEBUG
from engine.model import Model
from engine.storage import Storage

from interface.views.main_menu_view import MainMenuView
from content.areas.test_forest import test_forest

from .confirm_modal_state import ConfirmModalState
from .state import State, T, SaveAndQuit, EffectsBreak


class MainMenuState(State[None]):
    """Main Menu"""

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
                self.start()
            else:
                if DEBUG:
                    print("Storage: No data for this slot.")
                self.new_game()

        elif event.sym == tcod.event.K_ESCAPE:
            pass

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
        else:
            return super().ev_keydown(event)

    def new_game(self) -> None:
        try:
            self._model = Model()
            self._model.area_data.current_area = test_forest(self._model)
            self.storage.add_save(self._view.character_select.index_as_int,
                                  self.model)
            self.start()
        except SystemExit:
            print("Failed to start game!")
            raise

    def start(self) -> None:
        assert self.model
        try:
            self.model.loop()
        except SaveAndQuit:
            self.storage.write_to_file()
        except SystemExit:
            self.storage.write_to_file()
        except EffectsBreak:
            self.storage.write_to_file()
            self.start()
