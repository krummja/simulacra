from __future__ import annotations  # type: ignore
from typing import Optional, TYPE_CHECKING

from enum import Enum


class Symmetry(Enum):
    NONE = 1
    MIRROR_H = 2
    MIRROR_V = 3
    MIRROR_B = 4
    ROTATE_90 = 5
    ROTATE_180 = 6



def furnishing(
        freq: Optional[float], 
        symmetry: Optional[Symmetry], 
        template: Optional[str]
    ) -> None:
    furnishing_freq = freq
    if symmetry is None:
        symmetry = Symmetry.NONE
    
    lines = template.split("\n")
    lines = map(lambda line : list(line.trim()), lines)


def mirror_char_horizontal(input: str) -> str:
    pass

def mirror_char_vertical(input: str) -> str:
    pass

def rotate_char_90(input: str) -> str:
    pass