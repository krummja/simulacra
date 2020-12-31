"""ENGINE.COMPONENTS.Stats"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from engine.entities import Stat, StatsEnum

from .component import Component

if TYPE_CHECKING:
    from engine.entities.entity import Entity


class Stats(Component):
    """Stats component"""

    def __init__(self, **kwargs) -> None:
        super().__init__("STATS")
        self._core_stats: Dict[StatsEnum, Stat] = {}
        for k, v in kwargs.items():
            self.add_core_stat(StatsEnum[k.capitalize()], v, v)

    def add_core_stat(
            self,
            stat: StatsEnum,
            current_value: int,
            maximum_value: int
        ) -> None:
        if stat in StatsEnum:
            self._core_stats[stat] = Stat(stat,
                                          current_value,
                                          maximum_value)

    def modify_core_current_value(
            self,
            stat: StatsEnum,
            modifier: int
        ) -> None:
        if stat in self._core_stats:
            self._core_stats[stat].current += modifier

    def set_core_current_value(
            self,
            stat: StatsEnum,
            current_value: int
        ) -> None:
        if stat in self._core_stats:
            self._core_stats[stat].current = current_value

    def set_core_maximum_value(
            self,
            stat: StatsEnum,
            maximum_value: int
        ) -> None:
        if stat in self._core_stats:
            self._core_stats[stat].maximum = maximum_value

    def set_total_core_value(
            self,
            stat: StatsEnum,
            value: int
        ) -> None:
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

    def copy(self) -> Stats:
        copy_instance = Stats()
        copy_instance._core_stats = self._core_stats.copy()
        return copy_instance


def initialize_character_stats(
        health=10,
        might=10,
        finesse=10,
        intellect=10,
        size=5,
        **kwargs
    ) -> Stats:
    stats = Stats()
    stats.add_core_stat(StatsEnum.Health, health, health)
    stats.add_core_stat(StatsEnum.Might, might, might)
    stats.add_core_stat(StatsEnum.Finesse, finesse, finesse)
    stats.add_core_stat(StatsEnum.Intellect, intellect, intellect)
    stats.add_core_stat(StatsEnum.Size, size, size)
    if kwargs:
        pass
    return stats
