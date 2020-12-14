from __future__ import annotations

import tcod
from typing import Optional, TYPE_CHECKING
from collections import UserString
from hues import set_color, RESET


class Message:

    def __init__(self, msg: str) -> None:
        self.msg = msg
        self.count = 1

    def __str__(self) -> str:
        if self.count > 1:
            return f"{self.msg} (x{self.count})"
        return self.msg


class ColorFormatter:

    def __init__(self, color: Tuple[int, int, int]) -> None:
        self.color = color
    
    def format(self, string: str) -> ConsoleText:
        fg = self.color
        length = len(string)
        string = f"{tcod.COLCTRL_FORE_RGB:c}{fg[0]:c}{fg[1]:c}{fg[2]:c}" + string + f"{RESET}"
        return ConsoleText(string, length)
    
        
class ConsoleText(UserString):
    
    def __init__(self, seq, length: int) -> None:
        super().__init__(seq)
        self._seq = seq
        self._length = length
        
    def __len__(self) -> int:
        return self._length
    
    def __add__(self, other):
        length = self._length + len(other)
        return ConsoleText(self.data + other, length)
    
    def __radd__(self, other):
        length = self._length + len(other)
        return ConsoleText(other + self.data, length)
    