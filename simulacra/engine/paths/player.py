from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING


from engine.paths import Fighter


class Player(Fighter):
    name = "Player"
    char = ord("@")
    color = (255, 0, 255)

    hp = 30
    power = 5
    defense = 2