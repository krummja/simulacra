from __future__ import annotations
from typing import Dict, Optional, Tuple, TYPE_CHECKING

from collections import defaultdict

from hues import COLOR

if TYPE_CHECKING:
    from model import Model
    from tcod.console import Console


class ElementConfig(defaultdict):
    
    def __init__(
            self,
            uid: str = "<unset>",
            x: int = 0, 
            y: int = 0,
            width: int = 0,
            height: int = 0,
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (0, 0, 0),
            title: Optional[str] = None,
            framed: bool = False
        ) -> None:
        self.UID = uid
        self['x'] = x
        self['y'] = y
        self['width'] = width
        self['height'] = height
        self['fg'] = fg
        self['bg'] = bg
        self['title'] = title
        self['framed'] = framed


class BaseElement:
    
    def __init__(self, config: ElementConfig) -> None:
        for k, v in config.items():
            self.__setattr__(k, v)
    
    def on_draw(self, consoles: Dict[str, Console]) -> None:
        self.draw(consoles)
        self.draw_content(consoles)

    def draw(self, consoles: Dict[str, Console]) -> None:
        if self.framed:
            consoles['ROOT'].draw_frame(
                x=self.x, y=self.y, 
                width=self.width, height=self.height, 
                fg=self.fg, bg=self.bg
                )
            
        if self.title:
            consoles['ROOT'].print(
                x=self.x+2, y=self.y,
                string=f" {self.title} "
                )

    def draw_content(self, consoles: Dict[str, Console]) -> None:
        pass