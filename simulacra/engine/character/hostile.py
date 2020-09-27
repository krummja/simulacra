from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.hues import COLOR
from engine.character import Character


class Hostile(Character):

    char = ord("H")
    color = COLOR['red']
