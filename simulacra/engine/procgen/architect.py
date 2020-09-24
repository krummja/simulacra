from __future__ import annotations  # type: ignore
from typing import Iterator, Iterable, List, Tuple, Typle, TYPE_CHECKING

import random
import numpy as np
import tcod

from engine.character.player import Player
from engine.area import *
from engine.tile import *

if TYPE_CHECKING:
    from engine.actor import Actor
    from engine.location import Location
    from engine.model import Model


class Architect:

    def __init__(self) -> None:
        pass

    def build_stage(self) -> Iterable[str]:
        pass