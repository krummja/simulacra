from __future__ import annotations
from typing import TYPE_CHECKING
from utils.metaclasses import ComponentMeta

if TYPE_CHECKING:
    from simulacra.ecs.entity import Entity


class Component(metaclass=ComponentMeta):
    """All Components inherit from this class.

    A minimal Component is a subclass of this class with fieldnames provided for
    the properties list.
    """
    properties = []

    def __init__(self, **kwargs):
        bound = self.__signature__.bind(**kwargs)
        for name, val in bound.arguments.items():
            setattr(self, name, val)

    def __repr__(self):
        args = ', '.join(repr(getattr(self, name)) for name in self.properties)
        return type(self).__name__ + '(' + args + ')'

    def _on_attached(self, entity: Entity) -> None:
        pass

    def _on_detached(self) -> None:
        pass

    def _on_destroyed(self) -> None:
        pass

    def _on_event(self, evt) -> None:
        pass

    def remove(self, destroy: bool = True) -> None:
        pass
