from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from simulacra.core.options import *
from simulacra.utils.geometry import *

from .ui_manager import UIManager


@dataclass
class ElementConfig:
    name: str = None
    parent: Element = None
    position: Tuple[str, str] = ("center", "center")
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    offset_x: int = 0
    offset_y: int = 0
    margin: int = 0
    fg: Tuple[int, int, int] = (255, 255, 255)
    bg: Tuple[int, int, int] = (0, 0, 0)
    title: str = None
    framed: bool = False
    frame_fg: Tuple[int, int, int] = None


class Position(ElementConfig):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.frame_fg is None:
            self.frame_fg = self.fg
        if self.parent is None:
            self.parent = self

        _position = self._set_position()
        setattr(self, 'x', _position[1])
        setattr(self, 'y', _position[0])

        self.x += self.offset_x
        self.y += self.offset_y

    def _set_position(self):
        switch = self.parent is not self

        self.width -= self.margin
        self.height -= self.margin

        top = (
            self.margin,
            self.parent.y + self.margin
            )[switch]

        bottom = (
            CONSOLE_HEIGHT - self.height,
            self.parent.container.bottom - self.height
            )[switch]

        left = (
            self.margin,
            self.parent.x + self.margin
            )[switch]

        right = (
            CONSOLE_WIDTH - self.width,
            self.parent.container.right - self.width
            )[switch]

        h_center = (
            (CONSOLE_WIDTH - self.width) // 2,
            self.parent.x + ((self.parent.width - self.width) // 2)
            )[switch]

        v_center = (
            (CONSOLE_HEIGHT - self.height) // 2,
            self.parent.y + ((self.parent.height - self.height) // 2)
            )[switch]

        return {
            ('top', 'left'): (top, left),
            ('top', 'right'): (top, right),
            ('top', 'center'): (top, h_center),
            ('bottom', 'left'): (bottom, left),
            ('bottom', 'right'): (bottom, right),
            ('bottom', 'center'): (bottom, h_center),
            ('center', 'left'): (v_center, left),
            ('center', 'right'): (v_center, right),
            ('center', 'center'): (v_center, h_center)
            }.get(self.position)


class Element(Position):

    def __init__(self, manager: UIManager, **kwargs) -> None:
        super().__init__(**kwargs)
        self.manager = manager
        self.console = self.manager.game.renderer.root_console

    @property
    def container(self) -> Rect:
        return Rect.from_edges(
            top=self.y,
            bottom=self.y + self.height,
            left=self.x,
            right=self.x + self.width,
            )

    @property
    def content(self) -> Rect:
        return Rect.from_edges(
            top=self.container.top + 1,
            bottom=self.container.bottom - 1,
            left=self.container.left + 2,
            right=self.container.right - 1,
            )

    def on_render(self, dt) -> None:
        # self.draw_frame()
        self.draw_content(dt)

    def draw_frame(self) -> None:
        console = self.manager._game.renderer.root_console
        if self.framed:
            pass
        if self.title:
            pass

    def draw_content(self, dt) -> None:
        pass
