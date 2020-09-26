from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING

from engine.hues import COLOR
from engine.character import Character


class NPC(Character):

    char = ord("N")
    color = COLOR['yellow']
