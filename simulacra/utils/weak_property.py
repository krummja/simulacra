from __future__ import annotations
import weakref


class WeakProperty:

    def __init__(self, name: str) -> None:
        self.name = name

    def __get__(desc, self, cls):
        if self is None:
            return desc
        try:
            ref = self.__dict__[desc.name]
        except KeyError:
            return None
        else:
            value = ref()
            if value is None:
                del self.__dict__[desc.name]
            return value

    def __set__(desc, self, value) -> None:
        self.__dict__[desc.name] = weakref.ref(value)

    def __delete__(desc, self):
        del self.__dict__[desc.name]
