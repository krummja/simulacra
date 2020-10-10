from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from config import *
from storage import Storage
from states import State, T, SaveAndQuit, GameOverQuit

from engine.generation.test_area import test_area
from engine.model import Model

from interface.character_menu import CharacterMenu
from interface.help_text import HelpText
from interface.logo import draw_logo

if TYPE_CHECKING:
    from tcod.console import Console


class MainMenu(State[None]):

    def __init__(self: MainMenu) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.storage = Storage()
        self.storage.load_from_file()

        load_slot = "[enter] continue, "
        create_new = "[enter] create new, "
        self.help_text = HelpText(content=[
            load_slot if self.storage.save_slots[0] is not None else create_new,
            "[⬆/⬇/⬅/➡] change selection, ",
            "[d] delete, ",
            "[q] quit"
            ])

        self.character_menu = CharacterMenu(
            position=("top", "left"),
            width=CONSOLE_WIDTH, height=CONSOLE_HEIGHT
            )

        self.character_menu.data_source = self.storage

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(consoles)

        self.character_menu.on_draw(consoles)

        self.help_text.on_draw(consoles)

    def ev_keydown(self: MainMenu, event: tcod.event.KeyDown) -> Optional[T]:
        key = event.sym
        index = self.character_menu.index_as_int

        if key == tcod.event.K_q:
            self.cmd_quit()

        elif key == tcod.event.K_d:
            if self.storage.save_slots[index] is not None:
                self.storage.save_slots[index] = None
            self.storage.write_to_file()

        elif key == tcod.event.K_RETURN:
            menu_data = self.character_menu.data_at_index
            if menu_data is None:
                self.new_game()
            else:
                self.model = self.storage.save_slots[index]
                self.start()

        elif key == tcod.event.K_ESCAPE:
            pass

        elif event.sym in self.MOVE_KEYS:
            self.character_menu.current_index = (
                self.MOVE_KEYS[event.sym][0],
                self.MOVE_KEYS[event.sym][1]
                )

        else:
            super().ev_keydown(event)

    def new_game(self: MainMenu) -> None:
        try:
            self.model = Model()
            self.model.current_area = test_area(self.model)
            self.storage.add_save(self.character_menu.index_as_int, self.model)
            self.start()
        except SystemExit:
            raise

    def start(self: MainMenu) -> None:
        assert self.model
        try:
            self.model.loop()
        except SaveAndQuit:
            self.storage.write_to_file()
        except GameOverQuit:
            self.model = None
        except SystemExit:
            self.storage.write_to_file()

