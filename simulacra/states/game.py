from __future__ import annotations  # type: ignore
from typing import Any, Generic, Optional, TypeVar, TYPE_CHECKING, Tuple

import tcod
import tcod.console as Console

from simulacra.engine.actions import common
from simulacra.engine.rendering import *
from . import State, StateBreak

if TYPE_CHECKING:
    from simulacra.engine import actions
    from simulacra.engine.model import Model
    from simulacra.engine.item import Item

T = TypeVar("T")


class AreaState(Generic[T], State[T]):
    pass


class PlayerReady(AreaState["actions.Action"]):
    pass


class BaseInventoryMenu(AreaState["actions.Action"]):
    pass


class UseInventory(BaseInventoryMenu):
    pass


class DropInventory(BaseInventoryMenu):
    pass


class PickLocation(AreaState[Tuple[int, int]]):
    pass