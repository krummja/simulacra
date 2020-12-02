from __future__ import annotations
from typing import Dict, Optional, TYPE_CHECKING

import tcod
from config import *

from view import View
from views.elements.base_element import BaseElement, ElementConfig

if TYPE_CHECKING:
    from tcod.console import Console
    from state import State


class BaseModalView(View, BaseElement):
    
    def __init__(self, state: State, config: ElementConfig) -> None:
        View.__init__(self, state)
        BaseElement.__init__(self, config)
