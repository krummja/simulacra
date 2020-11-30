from __future__ import annotations
from typing import Any, Tuple, Dict, Optional, Protocol, TYPE_CHECKING
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

