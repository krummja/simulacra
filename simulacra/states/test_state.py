from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod
from states import State, T
from engine.model import Model
from engine.generation.test_area import test_area

if TYPE_CHECKING:
    from tcod.console import Console


class TestState(State[None]):

    def __init__(self: TestState) -> None:
        super().__init__()
        self.model = Model()
        self.model.current_area = test_area(self.model)

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(1, 1, "Hello, world!")

    def ev_keydown(self: TestState, keycode: tcod.event.KeyDown) -> Optional[T]:
        key = keycode.sym
        if key == tcod.event.K_ESCAPE:
            self.cmd_quit()
        elif key == tcod.event.K_RETURN:
            assert self.model
            try:
                self.model.loop()
            except SystemExit:
                raise
        else:
            super().ev_keydown(keycode)
        return None

    def cmd_quit(self) -> None:
        """Save and quit."""
        raise SystemExit()
