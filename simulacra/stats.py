from __future__ import annotations
from typing import TYPE_CHECKING
from enum import Enum


class StatsEnum(Enum):
    Health = 'health'
    Energy = 'energy'
    Might = 'might'
    Finesse = 'finesse'
    Intellect = 'intellect'
    Sharpness = 'sharpness'
    Hardness = 'hardness'
    Weight = 'weight'
    Size = 'size'
    Potency = 'potency'
    MaxDamage = 'max_damage'
    MinDamage = 'min_damage'
    ArmorClass = 'armor_class'


class Size:
    Fine = 0
    Diminutive = 1
    Tiny = 2
    Small = 3
    Medium = 4
    Large = 5
    Huge = 6
    Gargantuan = 7
    Colossal = 8
