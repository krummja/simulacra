from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from model import Model
from state import State, T
from storage import Storage
from views import MainMenuView


class MainMenuState(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self._model: Optional[Model] = None
        self._storage: Storage = Storage()
        self._view = MainMenuView(self)

    @property
    def storage(self):
        return self._storage

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[T]:

        index = self._view.character_select.index_as_int

        if event.sym == tcod.event.K_RETURN:
            menu_data = self.storage.save_slots[index]
            if menu_data is not None:
                self._model = self.storage.save_slots[index]
                self.start()
            else:
                self.new_game()

        elif event.sym == tcod.event.K_d:
            if self.storage.save_slots[index] is not None:
                self.storage.save_slots[index] = None
            self.storage.write_to_file()

        elif event.sym == tcod.event.K_q:
            self.cmd_quit()

        elif event.sym in self.MOVE_KEYS:
            self._view.character_select.current_index = (
                self.MOVE_KEYS[event.sym][1],
                self.MOVE_KEYS[event.sym][0]
            )

        return super().ev_keydown(event)

    def new_game(self) -> None:
        try:
            self._model = Model()
        except SystemExit:
            raise

    def start(self) -> None:
        assert self.model
        try:
            self.model.loop()
        except SystemExit:
            pass
