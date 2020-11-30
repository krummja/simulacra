from __future__ import annotations
from typing import Dict, Any, Tuple, Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class Component:
    """Components represent the interactive attributes of an entity.
    
    Every component should provide at least one option to present to any UI
    element that targets that component. For example, an Inventory component
    should provide a 'view' option that will appear in any menu raised as the
    result of an examine action.
    """

    NAME: str = '<unset>'

    def __init__(self, **kwargs):
        self.owner = None
        self._data = {}
        
    @property
    def data(self) -> Dict[str, Any]:
        return self._data
    
    @data.setter
    def data(self, value) -> None:
        """Update a data value. Uses a tuple ('key', value)."""
        self._data[value[0]] = value[1]

    def on_register(self, owner: Entity) -> None:
        self.owner = owner

    def on_unregister(self) -> None:
        self.owner = None
