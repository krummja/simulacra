from __future__ import annotations
from typing import Optional, Tuple, Type

from engine.actions.behaviors import Behavior
from engine.actor import Actor
from engine.game_object import GameObject
from engine.location import Location


class Item(GameObject):

    def __init__(
            self: Item,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            carryable: bool,
            equippable: bool
        ) -> None:
        super().__init__(char, color, bg, noun_text, location)
        self.carryable = carryable
        self.equippable = equippable

    @classmethod
    def spawn(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            carryable: bool,
            equippable: bool
        ) -> Item:
        self = cls(char, color, bg, noun_text, location, carryable, equippable)
        try:
            location.area.items[location.xy].append(self)
        except KeyError:
            location.area.items[location.xy] = [self]
        return self

    @classmethod
    def spawn_actor(
            cls,
            char: int,
            color: Tuple[int, int, int],
            bg: Tuple[int, int, int],
            noun_text: str,
            location: Location,
            behavior: Optional[Type[Behavior]],
            carryable: bool,
            equippable: bool
        ) -> Actor:
        self = cls(char, color, bg, noun_text, location, carryable, equippable)
        actor = Actor(location, self, behavior)
        self.location.area.actors.add(actor)
        return actor
