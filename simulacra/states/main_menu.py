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
from interface.logo import draw_logo

if TYPE_CHECKING:
    import tcod.console as Console


class MainMenu(State[None]):

    def __init__(self) -> None:
        super().__init__()
        self.model: Optional[Model] = None
        self.continue_message = "No characters! Please create a new one."

        test_rect = Rect.from_edges(top=3, bottom=10, left=3, right=10)
        print(test_rect.area)
        print(test_rect.indices)

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        # draw_logo(0, 0, consoles)

        interface_test(consoles)

        # test_modal = Modal(width=30, height=10, fg=(255, 50, 50), bg=(20, 20, 20))
        # test_modal.title = "test modal"
        # test_modal.on_draw(consoles)

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


def interface_test(consoles: Dict[Console]):
    
    right_panel_width = 30
    right_panel_height = CONSOLE_HEIGHT

    right_panel = Panel(
        position=("center", "right"),
        width=right_panel_width,
        height=right_panel_height,
        bg=(40, 40, 40)
    )
    right_panel.on_draw(consoles)

    Panel(position=("top", "left"),
          parent=right_panel,
          width=28,
          height=10,
          margin=1,
          bg=(100, 40, 40)).on_draw(consoles)

    Panel(position=("top", "left"),
          parent=right_panel,
          width=10,
          height=10,
          margin=1,
          vertical_offset=11,
          bg=(100, 100, 40)).on_draw(consoles)

    Panel(position=("bottom", "right"),
          parent=right_panel,
          width=14,
          height=10,
          margin=1,
        #   vertical_offset=11,
          bg=(100, 40, 100)).on_draw(consoles)

    Panel(position=("top", "right"),
          parent=right_panel,
          width=17,
          height=20,
          margin=1,
          vertical_offset=11,
          bg=(200, 0, 200)).on_draw(consoles)