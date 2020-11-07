from __future__ import annotations
from typing import Any, Dict, KeysView, ValuesView, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity


class ComponentData:

    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        self._keys: KeysView[str] = self.data.keys()
        self._values: ValuesView[Any] = self.data.values()

    @property
    def keys(self) -> KeysView[str]:
        return self._keys

    @property
    def values(self) -> ValuesView[Any]:
        return self._values

    def __repr__(self):
        return (f'{self.__class__.__name__}\n'
                f'Data:    {self.data!r}\n'
                f'Keys:    {self.keys!r}\n'
                f'Values:  {self.values!r}')

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        try:
            if self[key]:
                self.data[key] = value
        except KeyError(f"{key} does not exist in {self.__class__.__name__}"):
            raise


class Component(dict):
    """Base dict class to represent a component on an entity.
    Components are the tables that hold all of an entity's mutable data. They
    allow for a consistent data structure for accessing information relevant to
    game processes and UI representation.
    Accessing the component's data is done through the `Component.data`, which
    will return a `ComponentData` instance that mediates access to the internals
    of the selected component.
    """

    ident = '<unset>'

    def __init__(self, owner: Entity, config: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.owner = owner

        if config is not None:
            for key, value in config:
                self[key] = value

    @property
    def data(self):
        return ComponentData(self)

    def configure(self, **kwargs):
        raise NotImplementedError(f"{self.__class__.__name__} has no configuration!")
