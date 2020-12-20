from __future__ import annotations

import tcod
from typing import Optional, TYPE_CHECKING
from collections import UserString
from hues import set_color, RESET


class Message:

    def __init__(
            self, 
            msg: str,
            noun1: Optional[Noun] = None,
            noun2: Optional[Noun] = None,
            noun3: Optional[Noun] = None
        ) -> None:
        self.msg = self._format(msg, noun1=noun1, noun2=noun2, noun3=noun3)
        self.count = 1
        
    def singular(self, text: str) -> str:
        return self._categorize(text, is_first = True)

    def conjugate(self, text: str, pronoun: Pronoun) -> str:
        if pronoun == Pronoun.you or pronoun == Pronoun.they:
            is_first = True
            return _categorize(text, is_first = is_first)
        return _categorize(text)

    def quantify(self, text: str, count: int) -> str:
        pass

    def _format(
            self,
            text: str,
            noun1: Optional[Noun] = None,
            noun2: Optional[Noun] = None,
            noun3: Optional[Noun] = None
        ) -> str:
        result = text
        
        nouns = [noun1, noun2, noun3]
        for i in range(len(nouns)):
            noun = nouns[i - 1]
            if noun is not None:
                result = result.replace(f'{i}', noun.noun_text)
                
                result = result.replace("they", noun.pronoun.nom)
                result = result.replace("them", noun.pronoun.obl)
                result = result.replace("their", noun.pronoun.gen)
            
        if noun1 is not None:
            result = self.conjugate(result, noun1.pronoun)

        return result
    
    def _categorize(
            self, 
            text: str, 
            is_first: bool = False, 
            force: bool = False
        ) -> str:
        pass        

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
    