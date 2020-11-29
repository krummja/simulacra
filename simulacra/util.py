from __future__ import annotations
from typing import Dict, Optional, Protocol, TYPE_CHECKING
from contextlib import suppress
import collections
import time
import functools


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python?noredirect=1&lq=1
class Singleton(type):
    _instances = {}
    def __cls__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls
                ).__call__(*args, **kwargs)
            return cls._instances[cls]
        

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # Execute the called function
            return func(*args, **kwargs)
        except Exception as e:
            error_msg = 'An error has occurred at /' + func.__name__ + '\n'
            return e
    return wrapper


class Subject:

    def __init__(self) -> None:
        self._observers: Dict[str, Observer] = {}

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers.values():
            self._observers[observer.NAME] = observer
            
    def detach(self, observer_name: str) -> None:
        with suppress(ValueError):
            del self._observers[observer_name]
    
    def notify(self, modifier: Optional[Observer] = None) -> None:
        for observer in self._observers.values():
            if modifier != observer:
                observer.update(self)


class Observer(Protocol):

    NAME = "<unset>"

    def update(self, subject) -> None:
        pass


class Data(Subject):
    
    def __init__(self, name: str = "") -> None:
        super().__init__()
        self.NAME = name
        self._data = {}
        self._options = {}
    
    def get_data(self):
        return self._data
    
    def set_data(self, key, value) -> None:
        self._data[key] = value
        self.notify()
    
    @property
    def options(self):
        return self._options