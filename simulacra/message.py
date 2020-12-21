from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from collections import UserString

import re
import tcod

from hues import set_color, RESET

from noun import Pronoun

if TYPE_CHECKING:
    from noun import Noun


THEY = "nom"
THEM = "obl"
THEIR = "gen"


class Message:

    def __init__(
            self, 
            text: str,
            noun1: Optional[Noun] = None,
            noun2: Optional[Noun] = None,
            noun3: Optional[Noun] = None
        ) -> None:
        self.text = self._format(text, noun1=noun1, noun2=noun2, noun3=noun3)
        self.count = 1
        
    def singular(self, text: str) -> str:
        return self._categorize(text, is_first = True)

    def conjugate(self, text: str, pronoun: Pronoun) -> text:
        if pronoun == Pronoun.you or pronoun == Pronoun.they:
            return self._categorize(text, is_first=True)
        return self._categorize(text)

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
            noun = nouns[i]
            if noun is not None:
                
                result = result.replace(f'{i}', noun.noun_text)

                result = result.replace(f"({noun.noun_text}, 'nom')", noun.pronoun().nom)
                result = result.replace(f"({noun.noun_text}, 'obl')", noun.pronoun().obl)
                result = result.replace(f"({noun.noun_text}, 'gen')", noun.pronoun().gen)

        if noun1 is not None:
            result = self.conjugate(result, noun1.pronoun)

        return result[0].upper() + result[1:]
    
    def _categorize(
            self, 
            text: str, 
            is_first: bool = False, 
            force: bool = False
        ) -> str:
        assert is_first is not None
        
        optional_suffix = "\[(\w+?)\]"
        irregular = "\[([^|]+)\|([^\]]+)\]"
        
        # If it's a regular word in second category, add "s"
        if force and not is_first and text.find("[") != -1:
            return f"{text}s"
        
        # Handle words with optional suffixes like `close[s]` and `sword[s]`.
        while True:
            match = re.search(optional_suffix, text)
            if match is None:
                break
            
            before = text[0:match.span()[0]]
            after = text[match.span()[1]:]
            
            if is_first:
                text = f"{before}{after}"
            else:
                text = f"{before}{match[1]}{after}"
        
        # And now handle irregulars
        while True:
            match = re.search(irregular, text)
            if match is None:
                break
            
            before = text[0:match.span()[0]]
            after = text[match.span()[1]:]
            
            if is_first:
                text = f"{before}{match[1]}{after}"
            else:
                text = f"{before}{match[2]}{after}"
            
        return text

    def __str__(self) -> str:
        if self.count > 1:
            return f"{self.text} (x{self.count})"
        return self.text


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
    