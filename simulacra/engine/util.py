# pylint: skip-file
from __future__ import annotations

import math
import numpy as np
import collections
import functools
import weakref
from contextlib import suppress
from typing import Dict, Optional


class classproperty:
    """Implementation of class properties. Handy!"""
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)


def flatten(d, parent_key='', sep='_'):
    """Handy little function for hammering out nested dicts."""
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
    """Metaclass for implementing Singletons."""

    _instances = {}
    def __cls__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls
                ).__call__(*args, **kwargs)
            return cls._instances[cls]


class Flyweight:
    _pool = weakref.WeakValueDictionary()

    def __new__(cls, model) -> Flyweight:
        obj = cls._pool.get(model)
        if obj is None:
            obj = object.__new__(Flyweight)
            cls._pool[model] = obj
            obj.model = model
        return obj

    def __repr__(self):
        return f"<Flyweight: {self.model}>"


def vector2(x: int, y: int) -> np.ndarray:
    return np.array((x, y), dtype=np.float)

def magnitude(vec: np.ndarray) -> float:
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])

def normalize_vector(vec: np.ndarray) -> np.ndarray:
    m = magnitude(vec)
    if m > 0:
        return vec / m
