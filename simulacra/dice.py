from __future__ import annotations


class Dice:

    __slots__ = ['sides']

    def __init__(self, sides) -> None:
        self.sides = sides


class DiceStack:

    __slots__ = ['amount', 'dice']

    def __init__(self, amount, dice) -> None:
        self.amount = amount
        self.dice = dice
