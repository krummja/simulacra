from typing import Union


def mod(n: Union[int, float], m: Union[int, float]) -> Union[int, float]:
    return ((n % m) + m) % m
