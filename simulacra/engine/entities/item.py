"""ENGINE.ENTITIES.Item"""
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional

from .entity import Entity

if TYPE_CHECKING:
    from engine.events import Action, ActionWithItem
    from engine.components.component import Component
    from engine.areas import Location


class Item(Entity):
    """Item base class."""

    def __init__(
            self,
            uid: str = "",
            name: str = "",
            description: str = "",
            location: Optional[Location] = None,
            display: Optional[Dict[str, Any]] = None,
            slot: Optional[str] = None
        ) -> None:
        super().__init__(uid, location)

        # Basic properties
        self.owner = None
        self.location = location
        self._noun_text = name
        self._description = description

        # Display Properties
        self.char = display['char']
        self.color = display['color']
        self.bg = display['bg']

        self.slot = slot

        self.is_equipped = False
        self.is_broken = False
        self.is_unknown = False

    @property
    def is_equippable(self) -> bool:
        if self.slot is None:
            return False
        if self.is_equipped:
            return False
        if self.is_broken:
            return False
        if self.is_unknown:
            return False
        return True

    @property
    def name(self) -> str:
        return self._noun_text

    @property
    def description(self) -> str:
        return self._description

    def copy(self):
        new_item = Item(
            self.uid,
            self._noun_text,
            self._description,
            self.location
            )
        return super().copy_to(new_item)

    def lift(self) -> None:
        """Remove this item from any of its containers."""
        if self.owner:
            self.owner.pop_item(self)
            self.owner = None
        if self.location:
            item_list = self.location.area.items[self.location.xy]
            item_list.remove(self)
            if not item_list:
                del self.location.area.items[self.location.xy]
            self.location = None

    def place(self, location: Location) -> None:
        """Place this item on the floor at the given location."""
        assert not self.location, "This item already has a location."
        assert not self.owner, "Can't be placed because this item is currently owned."
        self.location = location
        items = location.area.items
        try:
            self.bg = location.area.area_model.get_bg_color(*location.xy)
            items[location.xy].append(self)
        except KeyError:
            items[location.xy] = [self]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return (self.uid == other.uid,
                self.name == other.name,
                self.description == other.description)

    def __ne__(self, other: object):
        if not isinstance(other, Item):
            return NotImplemented
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.uid, self.name, self.description))


class ArmorCategory(Enum):
    Light = 0
    Medium = 1
    Heavy = 2


class WeaponCategory(Enum):
    Simple = 0
    Martial = 1
    Exotic = 2


class WeaponType(Enum):
    Melee = 0
    Ranged = 1


class WornLayer(Enum):
    Inner = 0
    Outer = 1
    Extra = 2
