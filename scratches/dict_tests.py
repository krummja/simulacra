from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

from collections import defaultdict

if TYPE_CHECKING:
    from entity import Entity


class ElementConfig(defaultdict):
    
    def __init__(self, x: int = 0, y: int = 0) -> None:
        self['x'] = x
        self['y'] = y


class BaseElement:
    
    def __init__(self, config: ElementConfig) -> None:
        for k, v in config.items():
            self.__setattr__(k, v)


test = BaseElement(ElementConfig(x=10, y=10))
print(vars(test))