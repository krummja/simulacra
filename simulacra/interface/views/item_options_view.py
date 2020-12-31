from __future__ import annotations
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from config import *

from interface.elements.base_element import BaseElement, ElementConfig
from .view import View
from .base_menu_view import BaseMenuView

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.entities.entity import Entity
    from engine.states.state import State


class ItemOptionsView(BaseMenuView):

    def __init__(self, state: State) -> None:
        super().__init__(
            state=state,
            config=ElementConfig(
                position=("top", "right"),
                width=(SIDE_PANEL_WIDTH // 2),
                height=len(state._options) + 4,
                offset_y=(SIDE_PANEL_HEIGHT // 2) - 1,
                fg=(255, 255, 255),
                title="",
                framed=True,
                frame_fg=(255, 0, 255)
                ))
