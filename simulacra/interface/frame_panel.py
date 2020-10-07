from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from config import *
from interface.panel import Panel

if TYPE_CHECKING:
    import tcod.console as Console


class FramePanel(Panel):

    _focused: bool = False

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
            bg: Tuple[int, int, int] = (0, 0, 0),
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

    @property
    def focused(self: FramePanel) -> bool:
        return self._focused

    @focused.setter
    def focused(self: FramePanel, value: bool) -> None:
        self._focused = value

    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['INTERFACE'].draw_frame(
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
            fg=self.fg,
            bg=self.bg
            )

        consoles['INTERFACE'].print(
            x=self.x+2,
            y=self.y,
            string=self.title
            )

        consoles['INTERFACE'].blit(
            dest=consoles['ROOT'],
            dest_x=self.x,
            dest_y=self.y,
            src_x=self.x,
            src_y=self.y,
            width=self.width,
            height=self.height,
            )
