from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

import tcod.console
from config import *

if TYPE_CHECKING:
    import tcod.console as Console
    from engine.model import Model


def draw_main_view(model: Model, consoles: Dict[str, Console]) -> None:
    player = model.player

    if player.location:
        model.current_area.camera_pos = player.location.xy

    consoles['ROOT'].clear()
    model.current_area.render(consoles)


def draw_log(model: Model, consoles: Dict[str, Console]) -> None:
    i = 0

    for text in model.log[::-1]:
        i += tcod.console.get_height_rect(40, str(text))
        if i >= 10:
            break
        consoles['ROOT'].print_box(
            1, 45 - i, 40, 10, str(text), fg=(255, 255, 255), bg=(0, 0, 0)
            )
