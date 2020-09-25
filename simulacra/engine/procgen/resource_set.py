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

    def add(
            self, 
            object: T,
            name: Optional[str],
            depth: Optional[int],
            frequency: Optional[float],
            tags: Optional[str],
        ) -> None:
        self._add(object, name, depth, depth, frequency, frequency, tags)

    def add_ranged(
            self, 
            object: T,
            name: Optional[str],
            start: Optional[int],
            end: Optional[int],
            start_freq: Optional[float],
            end_freq: Optional[float],
            tags: Optional[str]
        ) -> None:
        self._add(object, name, start, end, start_freq, end_freq, tags)

    def _add(
            self, 
            object: T, 
            name: str, 
            start_depth: int, 
            end_depth: int, 
            start_freq: float, 
            end_freq: float, 
            tags: str
        ) -> None:
        if name is None:
            name = str(len(self.resources))
        if start_depth is None:
            start_depth = 1
        if end_depth is None:
            end_depth = start_depth
        if start_freq is None:
            start_freq = 1.0
        if end_freq is None:
            end_freq = start_freq

        for key in self.resources.keys():
            if key == name:
                raise Exception(f"Already have a resource named '{name}'.")

        resource: Resource = Resource(
            object, start_depth, end_depth, start_freq, end_freq)

        self.resources[name] = resource

        if tags is not None and tags != "":
            for tag_name in tags.split(" "):
                tag = self.tags.get(tag_name)
                if tag is None:
                    raise Exception(f"Unknown tag '{tag_name}'.")
                resource.tags.add(tag)
            
    def define_tags(self, paths: str) -> None:
        for path in paths.split(" "):
            parent: Tag[T] = None
            tag: Tag[T] = None
            for name in path.split("/"):
                tag = self.tags.get(name)
                if tag is None:
                    tag = Tag(name, parent)
                    print(vars(tag))
                    self.tags[name] = tag
                parent = tag

    def find(self, name: str) -> T:
        resource = self.resources[name]
        if resource is None:
            raise Exception(f"Unknown resource '{name}'.")
        return resource.object

    def try_find(self, name: str) -> Optional[T]:
        resource = self.resources[name]
        if resource is None:
            return None
        return resource.object

    def has_tag(self, name: str, tag_name: str) -> bool:
        """Returns whether the resource with `name` has `tag_name` as one of
        its immediate tags or one of their parents.
        """
        resource = self.resources[name]
        if resource is None:
            raise Exception(f"Unknown resource '{name}'.")
        tag = self.tags.get(tag_name)
        if tag is None:
            return False

        check = lambda this_tag : this_tag.contains(tag)
        result = [check(_) for _ in self.tags.values()]
        print(any(result))
        return any(result)

    def get_tags(self, name: str) -> Iterable[str]:
        resource = self.resources.get(name)
        if resource is None:
            raise Exception(f"Unknown resource '{name}'.")
        return [tag.name for tag in resource.tags]

    def tag_exists(self, tag_name: str) -> bool:
        result = [tag_name == tag for tag in self.tags]
        return any(result)

    def try_choose(self, depth: int) -> None:
        pass

    def try_choose_matching(
            self, depth: int, tags: Iterable[str]) -> Optional[T]:
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
        while this_tag is not None:
            if tag == this_tag:
                return True
            this_tag = this_tag.parent
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

class SomeObject:

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

test_obj = SomeObject("Test")

test_set = ResourceSet()
test_res = Resource(test_obj, 0, 1, 1.0, 1.0)

# test_res.tags.add(Tag("sword"))
# test_res.tags.add(Tag("weapon"))
test_set.define_tags("equipment/weapon/sword item/potion/health_potion")

test_set.add(test_res, "test_resource", 0, 1.0, "weapon sword")

test_set.has_tag("test_resource", "sword")
print(test_set.get_tags("test_resource"))

print(test_set.tag_exists("sword"))

