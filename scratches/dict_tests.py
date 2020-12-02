from __future__ import annotations
from typing import Callable, List, TYPE_CHECKING

from collections import defaultdict

if TYPE_CHECKING:
    from entity import Entity


class SomeClass:
    
    def __init__(self) -> None:
        self.position = ('top', 'right')
        self.width = 10
        self.height = 10
        self.margin = 0
        self.parent = None
        
        pos = self.set_pos()
        self.__setattr__('x', pos[0])
        self.__setattr__('y', pos[1])
    
    def _position_values(self, pos: str):
        switch = self.parent is self
        values = {'top': (0 + self.margin, 0 + self.height + self.margin),
                  'bottom': (0 + self.height - self.margin, 0 - self.height)}
        return values[pos][switch]
        
    
    def set_pos(self):
        switch = self.parent is self
        positions = {
            ('top', 'left'): (10, 10),
            ('top', 'right'): (10, 10),
            ('top', 'center'): (10, 10)
            }
        return positions[self.position][switch]
        #               ('top', 'left')[1] 

    @property
    def _top(self) -> int:
        return 0 + self.height

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

# test = SomeClass()
# print(test._position_values('bottom'))


switch = False
width = (10, 100)[switch] // 2
y = (width - 10) // 2

console_h = 50
console_w = 100

class Test:
    x = 0
    y = 0
    width = 10
    height = 10
    parent = self

test = Test()
#        (50        - 10)          // 2  = 20
test.x = (console_h - test.height) // 2

