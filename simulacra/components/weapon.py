from __future__ import annotations
from typing import Dict, TYPE_CHECKING

from component import Component
from dice import Dice, DiceStack
from combat.enums import DamageType

if TYPE_CHECKING:
    from entity import Entity


class Weapon(Component):
    
    def __init__(
            self,
            weapon_category=None,
            weapon_type=None,
            size=None,
            ammunition_uid=None,
            finesse=False,
            loading=False,
            normal_range=0,
            long_range=0,
            reach=False,
            thrown=False,
            two_handed=False,
            melee_damage_type=DamageType.Blunt,
            ranged_damage_type=None,
            damage_dice=DiceStack(1, Dice(1))
        ) -> None:
        super().__init__("WEAPON")
        self['weapon_category'] = weapon_category
        self['weapon_type'] = weapon_type
        self['size'] = size
        self['ammunition_uid'] = ammunition_uid
        self['finesse'] = finesse
        self['loading'] = loading
        self['normal_range'] = normal_range
        self['long_range'] = long_range
        self['reach'] = reach
        self['thrown'] = thrown
        self['two_handed'] = two_handed
        self['melee_damage_type'] = melee_damage_type
        self['ranged_damage_type'] = ranged_damage_type
        self['damage_dice'] = damage_dice
        
    def copy(self):
        return Weapon(**self)