from __future__ import annotations  # type: ignore
from typing import Dict, Generic, Iterable, List, Optional, TypeVar, TYPE_CHECKING, Set

import random
import math
import numpy as np


T = TypeVar("T")


class ResourceSet(Generic[T]):

    tags: Dict[str, Tag[T]] = {}
    resources: Dict[str: Resource[T]] = {}
    queries: Dict[QueryKey, ResourceQuery[T]] = {}

    @property
    def is_empty(self) -> bool:
        return len(self.resources) == 0

    @property
    def is_not_empty(self) -> bool:
        return len(self.resources) > 0

    @property
    def all(self) -> Iterable[T]:
        return [resource.object for resource in self.resources.values()]

    def add(self, object: T) -> None:
        pass

    def add_ranged(self, object: T) -> None:
        pass

    def _add(self, object: T, *, **kwargs) -> None:
        pass
            
    def define_tags(self, paths: str) -> None:
        pass

    def find(self, name: str) -> T:
        pass

    def try_find(self, name: str) -> Optional[T]:
        pass

    def has_tag(self, name: str, tag_name: str) -> bool:
        pass

    def get_tags(self, name: str) -> Iterable[str]:
        pass

    def tag_exists(self, tag_name: str) -> bool:
        pass

    def try_choose(self, depth: int, *, **kwargs) -> None:
        pass

    def try_choose_matching(self, depth: int, tags: Iterable[str]) -> Optional[T]:
        pass

    def run_query(self, name: str, depth: int, scale: float) -> T:
        pass


class Resource(Generic[T]):

    def __init__(
            self,
            object: T,
            start_depth: int,
            end_depth: int,
            start_freq: float,
            end_freq: float
        ) -> None:
        self.object = object
        self.start_depth = start_depth
        self.end_depth = end_depth
        self.start_freq = start_freq
        self.end_freq = end_freq

        self.tags: Set[Tag] = set()

    def frequency_at_depth(self, depth: int) -> float:
        if (self.start_depth == self.end_depth):
            return self.start_freq
        # TODO: I may need to adjust this so that it returns valid values
        # TODO: ...outside of the range given.
        return interpolate(
            depth, 
            [self.start_depth, self.end_depth], 
            [self.start_freq, self.end_freq]
        )
        
    def chance_at_depth(self, depth: int) -> float:
        if depth < self.start_depth:
            relative = self.start_depth - depth
            deviation  = 0.6 + depth * 0.2
            return math.exp(-0.5 * relative * relative / (deviation * deviation))

        elif depth > self.end_depth:
            relative = depth - self.end_depth
            deviation = 1.0 + depth * 0.1
            return math.exp(-0.5 * relative * relative / (deviation * deviation))
        
        else:
            return 1.0


class Tag(Generic[T]):

    def __init__(self, name: str, parent: Optional[Tag[T]]=None) -> None:
        self.name = name
        self.parent = parent

    def contains(self, tag: Tag[T]) -> bool:
        this_tag = self
        if this_tag != tag:
            while self.parent is not None:
                if self.parent == tag:
                    print(f"{tag.name} is parent to {this_tag.name}")
                    return True
                else:
                    print(f"{tag.name} is contained in {self.name}'s scope.'")
                    return self.parent.contains(tag)
            else:
                print(f"{tag.name} not found in {self.name}'s scope.'")
                return False

    def to_string(self) -> str:
        if self.parent is None:
            return self.name
        return f"{self.parent.name}/{self.name}"


class QueryKey:

    def __init__(self, name: str, depth: int) -> None:
        self.name = name
        self.depth = depth

    @property
    def hashcode(self):
        pass

    def is_equal(self, other: QueryKey) -> bool:
        assert isinstance(other, QueryKey)
        return self.name == other.name & self.depth == other.depth

    def to_string(self) -> str:
        return f"{self.name} ({self.depth})"


class ResourceQuery(Generic[T]):

    def __init__(
            self,
            depth: int,
            resources: List[Resource[T]],
            chances: List[float],
            total_chance: float
        ) -> None:
        self.depth = depth
        self.resources = resources
        self.chances = chances
        self.total_chance = total_chance

    def choose(self) -> Optional[T]:
        if len(self.resources) == 0:
            return None
        
        t = random.uniform(0.0, self.total_chance)
        first = 0
        last = len(self.resources) - 1

        while True:
            middle = (first + last) // 2
            if middle > 0 & t < self.chances[middle - 1]:
                last = middle - 1
            elif t < self.chances[middle]:
                return self.resources[middle].object
            else:
                first = middle + 1

    def dump(self, key: QueryKey) -> None:
        print(key)
        for i in range(len(self.resources)):
            chance = self.chances[i]
            if i > 0:
                chance -= self.chances[i - 1]
            percent = (100.0 * chance / self.total_chance)
            percent = to_string_as_fixed(percent, 5)
            percent = padleft(percent, 8)
            print(f"{percent} {self.resources[i].object}")


def to_string_as_fixed(n: float, fraction_digits: int) -> str:
    def truncate(n: float, fraction_digits: int) -> float:
        stepper = 10.0 ** fraction_digits
        return math.trunc(stepper * n) / stepper
    
    return str(truncate(n, fraction_digits))

def padleft(string: str, length: int) -> str:
    return string.rjust(length, '0')


from bisect import bisect_left



def interpolate(i: int, x_list: List[float], y_list: List[float]) -> float:
    UNDEF = -99.0
    assert len(x_list) == len(y_list)
    if np.all(np.diff(xp) > 0):
        return np.interp(i, x_list, y_list, right=UNDEF)
    else:
        return ValueError("x_list must be strictly increasing.")


# Tests
# 
# tag_1 = Tag("tag_1")
# tag_2 = Tag("tag_2", tag_1)
# tag_3 = Tag("tag_3", tag_2)

# print(vars(tag_2))
# print(tag_2.to_string())
# print(tag_2.contains(tag_1))

# print(tag_3.contains(tag_1))

xp = [1.0, 10.0]
fp = [10.0, 100.0]

test = interpolate(3, xp, fp)
print(test)