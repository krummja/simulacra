from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from engine.rendering.hues import ColorFormatter

from config import *
from engine.rendering.hues import set_color, RESET
from interface.elements.help_text_element import HelpTextElement
from interface.elements.character_select_element import CharacterSelectElement
from engine.rendering.noise import NoiseMachine
from .view import View

from engine.rendering.rendering import draw_logo, draw_frame

if TYPE_CHECKING:
    from tcod import Console
    from engine.states.state import State


class MainMenuView(View):

    index = 0

    def __init__(self, state: State) -> None:
        super().__init__(state)
        self.state = state
        self.character_select = CharacterSelectElement()
        self.character_select.data_source = state.storage

    def draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].clear()
        # draw_frame(consoles)
        draw_logo(consoles)

        credit = "powered by PYTHON TCOD"
        width = len(credit)
        consoles['ROOT'].print(
            x=(CONSOLE_WIDTH - width) // 2,
            y=1,
            string=credit,
            fg=(255, 0, 0)
            )

        self.character_select.draw(consoles)

        load = f"[ENTER]:continue, ".upper()
        new = "[ENTER]:create new, ".upper()
        load_new_option = load if self.state.storage.save_slots[
            self.character_select.index_as_int
        ] is not None else new
        selection_option = f"[{chr(8593)}/{chr(8595)}/{chr(8592)}/{chr(8594)}]:change selection, ".upper()
        delete_option = "[D]:delete, ".upper()
        quit_option = "[Q]:quit ".upper()

        help_text = HelpTextElement(
            help_options=[
                load_new_option,
                selection_option,
                delete_option,
                quit_option
                ],
            hue=(255, 0, 0))
        help_text.draw(consoles)
