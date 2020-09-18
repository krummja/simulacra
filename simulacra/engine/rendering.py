from __future__ import annotations  # type: ignore
from typing import Dict, Tuple, TYPE_CHECKING

import tcod.console

if TYPE_CHECKING:
    import tcod.console as Console
    from .model import Model


def draw_main_view(model: Model, consoles: Dict[str, Console]) -> None:
    player = model.player

    if player.location:
        model.current_area.camera_pos = player.location.xy
    
    consoles['ROOT'].clear()
    model.current_area.render(consoles)
    
    
def draw_log(model: Model, consoles: Dict[str, Console]) -> None:
    pass