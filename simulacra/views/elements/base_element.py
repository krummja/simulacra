from __future__ import annotations
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from config import *

if TYPE_CHECKING:
    from tcod.console import Console
    from model import Model


class BaseElement:
    """An interface BaseElement is a minimal UI element.
    
    The BaseElement class should not be extended or overridden. Instead,
    extend the BaseRenderable and pass that in through a template definition.
    """
    
    def __init__(
            self,
            uid: str,
            x: int = 0,
            y: int = 0,
            width: int = CONSOLE_WIDTH,
            height: int = 3,
            framed: bool = False,
            title: str = "",
            fg: Tuple[int, int, int] = (255, 255, 255),
            bg: Tuple[int, int, int] = (0, 0, 0),
        ) -> None:
        self.uid = uid
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.framed = framed
        self.title = title
        self.fg = fg
        self.bg = bg
        self._renderable: BaseRenderable = None
        
    @property
    def renderable(self) -> BaseRenderable:
        return self._renderable
    
    @renderable.setter
    def renderable(self, value: BaseRenderable) -> None:
        self._renderable = value
    
    def draw(self, consoles: Dict[str, Console]) -> None:
        if self._renderable is not None:
            self._renderable.draw_elements(consoles)
            self._renderable.draw_contents(consoles)


class BaseRenderable:
    
    def __init__(self, element: BaseElement) -> None:
        self.element = element
        self.x = self.element.x + 1
        self.y = self.element.y + 2 if len(self.element.title) > 0 else self.element.y + 1
        self.width = self.element.width - 2
        self.height = self.element.height - 2

    def draw_contents(self, consoles: Dict[str, Console]) -> None:
        """Overridable method for drawing Renderable contents.
        
        Anything that interfaces with game data should be implemented through
        override of this method.
        """
        consoles['ROOT'].print_box(
            x=self.x, y=self.y,
            width=self.width, height=self.height,
            string="<BASE RENDERABLE>",
            fg=self.element.fg, bg=self.element.bg
            )
    
    def draw_elements(self, consoles: Dict[str, Console]) -> None:
        """Draw the frame elements to the console. 
        This should generally not be overridden by a concrete Renderable.
        """
        if self.element.framed:
            consoles['ROOT'].draw_frame(
                x=self.element.x, y=self.element.y,
                width=self.element.width, height=self.element.height,
                fg=self.element.fg, bg=self.element.bg
                )
       
            if len(self.element.title) > 0:
                consoles['ROOT'].print(
                    x=self.element.x + 2, y=self.element.y,
                    string=self.element.title,
                    fg=self.element.fg, bg=self.element.bg
                )