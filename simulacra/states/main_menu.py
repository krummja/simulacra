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

        # x_center = CONSOLE_WIDTH // 2
        # y_center = CONSOLE_HEIGHT // 2

        # for x in range(0, CONSOLE_WIDTH):
        #     consoles['ROOT'].tiles_rgb[["bg"]][Point(x, y_center).ij] = [100, 0, 0]
        # for y in range(0, CONSOLE_HEIGHT):
        #     consoles['ROOT'].tiles_rgb[["bg"]][Point(x_center, y).ij] = [100, 0, 0]

        # x_grid = {
        #     0: 1,
        #     1: (CONSOLE_WIDTH // 4) * 1,
        #     2: (CONSOLE_WIDTH // 4) * 2,
        #     3: (CONSOLE_WIDTH // 4) * 3,
        #     4: (CONSOLE_WIDTH // 4) * 4
        # }

        # for x_pos in x_grid.values():
        #     for y in range(0, CONSOLE_HEIGHT):
        #         consoles['ROOT'].tiles_rgb[["bg"]][Point(x_pos, y).ij] = [100, 0, 0]

        character_panel = Panel(position=("bottom", "center"),
                                width=64,
                                height=20,
                                vertical_offset=-4,
                                bg=(50, 50, 50))

        slot1 = Panel(position=("top", "left"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=1,
                      bg=(50, 0, 0)).on_draw(consoles)

        slot2 = Panel(position=("top", "center"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      bg=(50, 0, 0)).on_draw(consoles)

        slot3 = Panel(position=("top", "right"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=-1,
                      bg=(50, 0, 0)).on_draw(consoles)

        slot4 = Panel(position=("bottom", "left"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=1,
                      bg=(50, 0, 0)).on_draw(consoles)

        slot5 = Panel(position=("bottom", "center"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      bg=(50, 0, 0)).on_draw(consoles)

        slot6 = Panel(position=("bottom", "right"),
                      parent=character_panel,
                      width=18,
                      height=8,
                      margin=1,
                      horizontal_offset=-1,
                      bg=(50, 0, 0)).on_draw(consoles)

        HelpText(content=[
            "[enter] select, ", 
            "[⬆/⬇/⬅/➡] change selection, ", 
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

