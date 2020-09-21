from __future__ import annotations  # type: ignore
from typing import Dict, Optional, TYPE_CHECKING

import tcod
import numpy as np

from constants import *
from engine.model import Model
from engine.area import Area
from engine.procgen.dungeon import *
from geometry import *

from states import State
from interface.panel import Panel
from interface.modal import Modal
from interface.help_text import HelpText
from interface.logo import draw_logo

if TYPE_CHECKING:
    import tcod.console as Console


class MainMenu(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.continue_message = "No characters! Please create a new one."

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        draw_logo(0, 0, consoles)

        character_panel = Panel(
            position=("bottom", "center"),
            width=20,
            height=20,
            vertical_offset=-4,
            bg=(50, 50, 50)
        )
        character_panel.on_draw(consoles)

        Panel(
            parent=character_panel,
            position=("center", "center"),
            width=20,
            height=5,
            bg=(100, 0, 0)
        ).on_draw(consoles)

        HelpText(content=[
            "[enter] select, ", 
            "[⬆/⬇] change selection, ", 
            "[n] create new, ", 
            "[d] delete, ",
            "[q] quit"
        ]).on_draw(consoles)

    def ev_keydown(self, event: tcod.event.KeyDown):
        key = event.sym
        
        if key == tcod.event.K_c and self.model:
            self.start()
        elif key == tcod.event.K_n:
            self.new_game()
        elif key == tcod.event.K_q:
            self.cmd_quit()
        else:
            super().ev_keydown(event)

    def new_game(self) -> None:
        self.model = Model()
        self.model.current_area = generate(self.model, 256, 256)
        self.start()
        
    def start(self) -> None:
        assert self.model
        try:
            self.model.loop()
        except SystemExit:
            raise
        self.continue_message = str(self.model)

    def save(self) -> None:
        pass

    def remove_save(self) -> None:
        pass

