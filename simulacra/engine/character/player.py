from __future__ import annotations  # type: ignore
from typing import TYPE_CHECKING


from engine.character import Character


class Player(Character):
    """An `Actor` factory which creates `Player` instances."""

    char = ord("@")
    color = (255, 0, 255)