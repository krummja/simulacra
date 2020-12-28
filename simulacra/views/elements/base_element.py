from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from collections import defaultdict

from hues import COLOR
from config import *
from geometry.rect import Rect

if TYPE_CHECKING:
    from model import Model
    from tcod.console import Console


class ElementConfig(defaultdict):
    
    def __init__(
            self,
            uid: str = "<unset>",
            parent = None,
            position: Tuple[str, str] = ("center", "center"),
            x: int = 0, 
            y: int = 0,
            width: int = 0,
            height: int = 0,
            offset_x: int = 0,
            offset_y: int = 0,
            margin: int = 0,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (0, 0, 0),
            title: Optional[str] = None,
            framed: bool = False,
            frame_fg: Optional[Tuple[int, int, int]] = None
        ) -> None:
        self.UID = uid
        self['parent'] = parent
        self['position'] = position
        self['x'] = x
        self['y'] = y
        self['width'] = width
        self['height'] = height
        self['offset_x'] = offset_x
        self['offset_y'] = offset_y
        self['margin'] = margin
        self['fg'] = fg
        self['bg'] = bg
        self['title'] = title
        self['framed'] = framed
        self['frame_fg'] = frame_fg


class Position:
    """Base class for handling GUI element positioning."""
    
    def __init__(self, config: ElementConfig) -> None:
        
        # TODO: Fix this
        for k, v in config.items():
            self.__setattr__(k, v)

        if config['frame_fg'] is None:
            self.frame_fg = self.fg

        if config['parent'] is None:
            self.parent = self

        _position = self._set_position()
        self.__setattr__('x', _position[1])
        self.__setattr__('y', _position[0])
        
        self.x += self.offset_x
        self.y += self.offset_y
        
    def _set_position(self):
        switch = self.parent is not self
        self.width = self.width - self.margin
        self.height = self.height - self.margin
        
        top = (
            self.margin, 
            self.parent.y + self.margin
            )[switch]
        
        bottom = (
            CONSOLE_HEIGHT - self.height, 
            self.parent.bounds.bottom - self.height
            )[switch]
        
        left = (
            self.margin, 
            self.parent.x + self.margin
            )[switch]
        
        right = (
            CONSOLE_WIDTH - self.width,
            self.parent.bounds.right - self.width
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
        

class BaseElement(Position):
    
    def __init__(self, config: ElementConfig) -> None:
        super().__init__(config)
    
    @property
    def bounds(self) -> Rect:
        return Rect.from_edges(top=self.y,
                               bottom=self.y + self.height,
                               left=self.x,
                               right=self.x + self.width)
        
    @property
    def content(self) -> Rect:
        return Rect.from_edges(top=self.bounds.top + 1,
                               bottom=self.bounds.bottom - 1,
                               left=self.bounds.left + 1,
                               right=self.bounds.right - 1)
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        self.draw_frame(consoles)
        self.draw_content(consoles)

    def draw_frame(self, consoles: Dict[str, Console]) -> None:
        if self.framed:
            consoles['ROOT'].draw_frame(
                x=self.x, y=self.y, 
                width=self.width, height=self.height, 
                fg=self.frame_fg, bg=self.bg
                )
            
        if self.title:
            consoles['ROOT'].print(
                x=self.x+2, y=self.y,
                string=f" {self.title} "
                )

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        pass

    

