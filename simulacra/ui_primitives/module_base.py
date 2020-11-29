from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from geometry import *
from util import Observer

if TYPE_CHECKING:
    from tcod.console import Console
    from ui_primitives.element_base import ElementBase


class ModuleBase(Observer):
    """A UI Module is a dynamic object that extends an Observer and has a 
    renderable.
    
    The Module's ElementBase is instantiated in a State class.
    """
    
    def __init__(
            self, 
            name: str = "<unset>", 
            element: ElementBase = None
        ) -> None:
        super().__init__()
        self.NAME = name
        self._element = element
        self._renderable: ModuleRenderable = None
        self._element.register_module(self)
    
    @property
    def renderable(self) -> ModuleRenderable:
        return self._renderable
    
    def update(self, subject) -> None:
        self._renderable.update(subject)


class ModuleRenderable:
    
    
    def __init__(self, module: ModuleBase) -> None:
        self._module = module
        self._module._renderable = self
        self._value: int = None
    
    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, value: int) -> None:
        self._value = value
    
    def update(self, subject):
        self._value = subject.get_data()['weight']
    
    def on_draw(self, consoles: Dict[str, Console]) -> None:
        consoles['ROOT'].print(3, 3, "Hello, world!", fg=(255, 255, 255))
        consoles['ROOT'].print(3, 5, f"{self._value}", fg=(255, 255, 255))