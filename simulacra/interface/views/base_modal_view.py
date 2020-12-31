from __future__ import annotations
from typing import TYPE_CHECKING

from config import *

from interface.views.view import View
from interface.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from engine.states.state import State


class BaseModalView(View, BaseElement):

    def __init__(self, state: State, config: ElementConfig) -> None:
        View.__init__(self, state)
        BaseElement.__init__(self, config)
