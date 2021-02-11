from __future__ import annotations
from typing import Generic, TypeVar, Tuple, Union

from simulacra.core.options import STAGE_WIDTH, STAGE_HEIGHT

import numpy as np


DType = TypeVar("DType")


class Array(np.ndarray, Generic[DType]):
    """Dummy class for type annotating NumPy ndarrays."""


def new_grid(
        shape: Tuple[int, int] = (STAGE_WIDTH, STAGE_HEIGHT),
        mask: bool = True,
        fill_value: int = 0
    ) -> Union[Array[np.bool], Array[np.str]]:
    dtype = np.bool if mask else np.str
    fill_value = fill_value if mask else object
    order = "F"
    # return np.full(shape=shape, fill_value=fill_value, dtype=dtype, order=order)
    return np.zeros(shape=shape, dtype=dtype, order=order)
