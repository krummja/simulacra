from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from geometry import *

if TYPE_CHECKING:
    from tcod.console import Console
    from ui_primitives.module_base import ModuleBase


class ElementBase:
    """A UI Element is a positionable and styleable rect.
    
    The Element is instantiated in a View class.
    
    The ElementBase acts as a bag of Observers that attach to Components.
    Each Observer is represented as a module of that ElementBase.
    Each module of the ElementBase should have at least one renderable.
    """
    
    def __init__(self, name: str = "<unset>") -> None:
        self.NAME = name
        self._modules = {}
        
    def register_module(self, module: ModuleBase) -> None:
        if module not in self._modules.items():
            self._modules[module.NAME] = module
        
    def unregister_module(self, module_name: str) -> None:
        if self._modules[module_name]:
            del self._modules[module_name]
        
    def draw(self, consoles: Dict[str, Console]) -> None:
        for module in self._modules.values():
            module.renderable.on_draw(consoles)
            