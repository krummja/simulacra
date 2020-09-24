from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

import tcod.console
from constants import *
from interface.panel import Panel

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
    log_width = SIDE_PANEL_WIDTH-2
    i = 0
    
    log_panel = Panel(position=("bottom", "right"),
                      width=log_width,
                      height=10,
                      margin=1,
                      bg=(0, 0, 0))
    log_panel.on_draw(consoles)
    
    x = log_panel.bounds.left
    y = log_panel.bounds.bottom

    for text in model.log[::-1]:
        i += tcod.console.get_height_rect(log_width, str(text))
        if i >= 10:
            break
        consoles['ROOT'].print_box(
            x, y - i, log_width, 0, str(text), fg=(255, 255, 255), bg=(0, 0, 0)
        )