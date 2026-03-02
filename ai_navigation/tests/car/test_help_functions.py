"""Unit tests for vector math helper functions.

Tests cover:
- Vector arithmetic (add, sub, mult, div)
- Vector operations (norm, normalize, scalar/cross product)
- Linear interpolation
- Edge cases (zero division, zero vectors)
"""

import math
from random import randint

from ai_navigation.src.car import add, div, lerp, mult, norm, normalize, scalar, sub


def r():
    """Generate random integer for testing.

    Returns:
        int: Random value between -10 and 10

    """
    return randint(-10, 10)


test_points = [((r(), r()), (r(), r())) for _ in range(250)]


def test_scalar() -> None:
    for a, b in test_points:
        assert (a[0] * b[1]) - (a[1] * b[0]) == scalar(a, b)


def test_sub() -> None:
    for a, b in test_points:
        assert (a[0] - b[0], a[1] - b[1]) == sub(a, b)


def test_div() -> None:
    for a, b in test_points:
        if b[0] == 0 and b[1] == 0:
            assert div(a, b) == (0, 0)
        elif b[0] == 0:
            assert (0, a[1] / b[1]) == div(a, b)
        elif b[1] == 0:
            assert (a[0] / b[0], 0) == div(a, b)
        else:
            assert (a[0] / b[0], a[1] / b[1]) == div(a, b)


def test_mult() -> None:
    for a, b in test_points:
        assert (a[0] * b[0], a[1] * b[1]) == mult(a, b)


def test_add() -> None:
    for a, b in test_points:
        assert (a[0] + b[0], a[1] + b[1]) == add(a, b)


def test_norm() -> None:
    for a, _ in test_points:
        assert math.sqrt(a[0] ** 2 + a[1] ** 2) == norm(a)


def test_normalize() -> None:
    for x, _ in test_points:
        scale = r()
        n = norm(x)
        if n == 0:
            assert normalize(x, scale) == (0, 0)
        else:
            assert (x[0] / n * scale, x[1] / n * scale) == normalize(x, scale)


def test_lerp() -> None:
    for _ in test_points:
        a = r()
        b = r()
        p = r()
        assert a + p * (b - a) == lerp(a, b, p)
