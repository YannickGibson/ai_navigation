from app.src.car.car import scalar, sub, div, mult, add, norm, normalize, lerp
from random import randint
import math


r = lambda : randint(-10, 10)
test_points = [ ((r(), r()), (r(), r())) for _ in range(250) ]

def test_scalar():
    for a, b in test_points:
        assert( (a[0] * b[1]) - (a[1] * b[0]) == scalar(a, b))

def test_sub():    
    for a, b in test_points:
        assert ((a[0] - b[0], a[1] - b[1]) == sub(a, b))

def test_div():
    for a, b in test_points:
        if b[0] == 0 and b[1] == 0: 
            assert( (0, 0) == div(a, b) )
        elif b[0] == 0 : 
            assert( (0, a[1] / b[1]) == div(a, b) )
        elif b[1] == 0 : 
            assert( (a[0] / b[0], 0) == div(a, b) )
        else:
            assert( (a[0] / b[0], a[1] / b[1]) == div(a, b) )
def test_mult():
    for a, b in test_points:
        assert( (a[0] * b[0], a[1] * b[1]) == mult(a, b))

def test_add():
    for a, b in test_points:
        assert( (a[0] + b[0], a[1] + b[1]) == add(a, b))

def test_norm():
    for a, _ in test_points:
        assert( math.sqrt(a[0]**2 + a[1]**2) == norm(a))

def test_normalize():
    for x, _ in test_points:
        scale = r()
        n = norm(x)
        if n == 0: assert ( (0, 0) == normalize(x, scale))
        else:
            assert( (x[0]/n * scale, x[1]/n * scale) == normalize(x, scale) )
def test_lerp():
    for _ in test_points:
        a = r()
        b = r()
        p = r()
        assert( a + p*(b-a) == lerp(a, b, p))
