from __future__ import annotations
from future.utils import with_metaclass

import decimal
import numpy as np

"""
Catmull-Rom splines are a family of cubic interpolating splines.
The tangent at each point p_i is calculated using the previous and next points
along the spline, defined as T(p_(i+1) - p_(i-1)). This is expressed as a
geometry matrix.
"""

spline_matrix = np.mat([[0, 0, 0, 0], 
                        [0, 0, 0, 0], 
                        [0, 0, 0, 0],
                        [0, 0, 0, 0]])


class Vector:
    x: float
    y: float


def float_range(start, stop, step):
    while start < stop:
        yield round(float(start), 1)
        start += float(decimal.Decimal(step))


def _spline(t, p0, p1, p2, p3):
    """Catmull-Rom cubic spline to interpolate 4 given points.
    
    Parameters:
        t       time index through the spline (must be 0-1)
        p0      previous point in the curve (for continuity)
        p1-p3   points to interpolate
    """
    return (t       *   ((2 - t) * t - 1)       * p0 +
            (t * t  *   (3 * t - 5) + 2)        * p1 + 
            t       *   ((4 - 3 * t) * t + 1)   * p2 +
            (t - 1) *   t * t                   * p3) / 2



range = [_ for _ in float_range(0.0, 1.0, '0.1')]
