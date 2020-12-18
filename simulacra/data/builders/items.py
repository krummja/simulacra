from __future__ import annotations
from typing import TYPE_CHECKING

from hues import COLOR
from item import Item, WeaponCategory, WeaponType
from data.materials import *
from components.weapon import Weapon
from components.stats import Stats
from dice import Dice, DiceStack
from stats import Size
from combat.enums import DamageType


def build_short_sword(area, location):
    _short_sword = Item(
        uid="short_sword",
        name="short sword",
        description="a short sword.",
        location=location,
        display={'char': ord("!"), 'color': COLOR['silver'], 'bg': (0, 0, 0)},
        slot='right_hand'
        )
    _short_sword.register_component(Iron.copy())
    _short_sword.register_component(Stats(health=1, size=Size.Medium))
    _short_sword.register_component(
        Weapon(weapon_category=WeaponCategory.Martial,
               weapon_type=WeaponType.Melee,
               size=Size.Small,
               melee_damage_type=DamageType.Pierce,
               damage_dice=DiceStack(1, Dice(6))))
    try:
        area.item_model.items[location.xy].append(_short_sword)
        _short_sword.bg = area.area_model.get_bg_color(*location.xy)
    except KeyError:
        area.item_model.items[location.xy] = [_short_sword]
    return area
        