from __future__ import annotations
from typing import Optional, Tuple

from config import *
from interface.panel import Panel
from interface.frame_panel import FramePanel


class EquipmentPanel(FramePanel):

    def __init__(
            self,
            position: Optional[Tuple[str, str]] = None,
            parent: Panel = None,
            width: int = CONSOLE_WIDTH,
            height: int = 0,
            margin: int = 0,
            vertical_offset: int = 0,
            horizontal_offset: int = 0,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (50, 50, 50),
            title: str=""
            ) -> None:
        super().__init__(
            position=position,
            parent=parent,
            width=width,
            height=height,
            margin=margin,
            vertical_offset=vertical_offset,
            horizontal_offset=horizontal_offset,
            fg=fg,
            bg=bg
            )
        self.title = title
