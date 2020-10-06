from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod

from states import State, T

from engine.generation.test_area import test_area
from engine.model import Model

from interface.help_text import HelpText
from interface.logo import draw_logo

if TYPE_CHECKING:
    from tcod.console import Console


class MainMenu(State[None]):

    def __init__(self: MainMenu) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.storage = None  # TODO: Implementation

        load_slot = "[enter] continue, "
        create_new = "[enter] create new, "
        self.help_text = HelpText(content=[
            create_new,
            "[⬆/⬇/⬅/➡] change selection, ",
            "[d] delete, ",
            "[q] quit"
            ])

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(consoles)
        self.help_text.on_draw(consoles)

    def ev_keydown(self: MainMenu, event: tcod.event.KeyDown) -> Optional[T]:
        key = event.sym

        if key == tcod.event.K_q:
            self.cmd_quit()

        elif key == tcod.event.K_RETURN:
            self.new_game()

        elif key == tcod.event.K_ESCAPE:
            pass

        else:
            super().ev_keydown(event)

    def new_game(self: MainMenu) -> None:
        try:
            self.model = Model()
            self.model.current_area = test_area(self.model)
            self.start()
        except SystemExit:
            raise

    def start(self: MainMenu) -> None:
        assert self.model
        try:
            self.model.loop()
        except SystemExit:
            raise

