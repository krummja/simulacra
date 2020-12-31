"""ENGINE.COMPONENTS.Inventory"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Dict, Hashable

from .component import Component

if TYPE_CHECKING:
    from engine.entities import Item


class ItemStack:
    """Representation of an inventory slot supporting multiple items."""

    def __init__(self, item: Item) -> None:
        self.amount = 1
        self.item = item

    def add_to_stack(self) -> None:
        self.amount += 1

    def pop_from_stack(self) -> Item:
        if self.amount:
            self.amount -= 1
        return copy.copy(self.item)

    def tuple(self):
        return self.item, self.amount

    def __hash__(self):
        return hash(self.item)

    @property
    def description(self):
        return self.item.description

    @property
    def name(self):
        return self.item.name

    def __str__(self) -> str:
        return str(self.tuple)


class Inventory(Component):
    """Inventory component"""

    def __init__(self) -> None:
        super().__init__("INVENTORY")
        self['item_stacks']: Dict[Hashable, ItemStack] = {}

    def add_item(self, item: Item):
        item.owner = self
        if item in self['item_stacks']:
            self['item_stacks'][item].add_to_stack()
        else:
            self['item_stacks'][item] = ItemStack(item)

    def pop_item(self, item: Item):
        if item in self['item_stacks']:
            popped_item = self['item_stacks'][item].pop_from_stack()
            if self['item_stacks'][item].amount <= 0:
                del self['item_stacks'][item]
            return popped_item

    def get_items(self, uid, count=0, pop=False):
        found_items = []
        item_stacks = [s for s in self['item_stacks'].values() if s.item.uid == uid]
        for stack in item_stacks:
            if count and len(found_items) >= count:
                break
            if pop:
                found_items.append(self.pop_item(stack.item))
            else:
                found_items.append(stack.item)
        return found_items

    def get_all_items(self):
        return self['item_stacks'].values()

    def __str__(self) -> str:
        return str([stack.item for stack in self.get_all_items()])
