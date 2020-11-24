from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from component import Component
from attribute import Attribute
from stats import StatsEnum
from attribute import Attribute

if TYPE_CHECKING:
    from entity import Entity


class Attributes(Component):

    ident = 'ATTRIBUTES'

    def __init__(self) -> None:
        super().__init__()
        self._core_stats: Dict[StatsEnum, Attribute] = {}

    def add_core_stat(
            self,
            stat: StatsEnum,
            current_value: int,
            maximum_value: int
        ) -> None:
        if stat in StatsEnum:
            self._core_stats[stat] = Attribute(stat, current_value, maximum_value)

    def modify_core_current_value(self, stat: StatsEnum, modifier: int) -> None:
        if stat in self._core_stats:
            self._core_stats[stat].current += modifier

    def set_core_current_value(self, stat: StatsEnum, current_value: int) -> None:
        if stat in self._core_stats:
            self._core_stats[stat].current = current_value

    def set_core_maximum_value(self, stat: StatsEnum, maximum_value: int) -> None:
        if stat in self._core_stats:
            self._core_stats[stat].maximum = maximum_value

    def set_total_core_value(self, stat: StatsEnum, value: int) -> None:
        self.set_core_current_value(stat, value)
        self.set_core_maximum_value(stat, value)

    def remove(self, stat: StatsEnum) -> None:
        if stat in self._core_stats:
            del self._core_stats[stat]

    def get_current_value(self, stat: StatsEnum) -> int:
        if stat in StatsEnum:
            stat_value = 0
            if stat in self._core_stats:
                stat_value += self._core_stats[stat].current

            # Responses

            return stat_value

    def copy(self) -> Attributes:
        copy_instance = Attributes()
        copy_instance._core_stats = self._core_stats.copy()
        return copy_instance


def initialize_character_attributes(
        health=0,
        might=0,
        finesse=0,
        intellect=0,
        size=5,
        **kwargs
    ) -> Attributes:
    attributes = Attributes()
    attributes.add_core_stat(StatsEnum.Health, health, health)
    attributes.add_core_stat(StatsEnum.Might, might, might)
    attributes.add_core_stat(StatsEnum.Finesse, finesse, finesse)
    attributes.add_core_stat(StatsEnum.Intellect, intellect, intellect)
    attributes.add_core_stat(StatsEnum.Size, size, size)
    return attributes