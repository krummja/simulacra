from __future__ import annotations
from typing import TYPE_CHECKING

from hues import COLOR
from item import Item


def build_short_sword():
    _short_sword = Item(uid="short_sword",
                        name="short sword",
                        description="a short sword.",
                        display={
                            'char': ord("!"), 
                            'color': COLOR['dark gray'], 
                            'bg': (0, 0, 0)},
                        slot="right_hand")
    return _short_sword