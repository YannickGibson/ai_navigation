

from app.src.car.car import Car, RotatingState
from pytest import approx

def test_move_0():
    c = Car(0, 0, 0)
    c.rotate_by(5)
    c.acc = 1
    c.move()
    assert (0.54 == approx(c.angle, 0.01))
    c.rotate_by(5)
    c.move()
    assert (1.98 == approx(c.angle, 0.01))
    c.rotate_by(5)
    c.move()
    assert (4.24 == approx(c.angle, 0.01))
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    assert (4.53 == approx(c.angle, 0.01))


def test_move_1():
    c = Car(10, 100, 60)
    c.rotate_by(5)
    c.acc = -1
    c.move()
    assert (59.46 == approx(c.angle, 0.01))
    c.rotate_by(5)
    c.move()
    assert (58.01 == approx(c.angle, 0.01))
    c.rotate_by(0)
    c.move()
    assert (56.80 == approx(c.angle, 0.01))
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    assert (56.95 == approx(c.angle, 0.01))

def test_move_2():
    c = Car(10, 100, 60)
    c.rotate_by(5)
    c.acc = -1
    c.move()
    assert (1.45 == approx(c.drift_angle, 0.01))
    c.rotate_by(5)
    c.move()
    assert (RotatingState.calm ==  c.rotating_state)
    c.rotate_by(0)
    c.move()
    assert (56.80 == approx(c.angle, 0.01))
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    assert (56.95 == approx(c.angle, 0.01))

def test_move_3():
    c = Car(10, 100, 60)
    c.rotate_by(5)
    c.acc = -1
    c.move()
    c.rotate_by(5)
    c.move()
    c.rotate_by(0)
    c.move()
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    assert (56.95 == approx(c.angle, 0.01))