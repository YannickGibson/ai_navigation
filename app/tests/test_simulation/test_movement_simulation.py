

from app.src.simulation.movement import MovementSimulation
from pytest import approx
import pygame


def test_movement_0():
    s = MovementSimulation(0)
    assert( 168 == s.car._x )
    go_forward = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_w})
    assert( False == s._register_keys(go_forward) )
    for _ in range(10):
        s._tick()
    assert( 171.92 == approx(s.car._x, .01) )
    
def test_movement_forward_backward():
    s = MovementSimulation(1)
    assert( 31.35 == approx(s.car.angle, .01) )
    assert( 208 == s.car._x )
    go_forward = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_w})
    assert( False == s._register_keys(go_forward) )
    for _ in range(10):
        s._tick()
    assert( 224.56 == approx(s.car._x, .01) )
    stop_forward = pygame.event.Event(pygame.KEYUP, {"key":pygame.K_w})
    assert( False == s._register_keys(stop_forward) )
    go_backward = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_s})
    assert( False == s._register_keys(go_backward) )
    for _ in range(50):
        s._tick()
    assert( 88.59 == approx(s.car._x, .01) )

def test_inertia():
    s = MovementSimulation(1)
    assert( 31.35 == approx(s.car.angle, .01) )
    assert( 208 == s.car._x )
    go_forward = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_w})
    assert( False == s._register_keys(go_forward) )
    for _ in range(10):
        s._tick()
    assert( 224.56 == approx(s.car._x, .01) )
    stop_forward = pygame.event.Event(pygame.KEYUP, {"key":pygame.K_w})
    assert( False == s._register_keys(stop_forward) )
    for _ in range(100):
        s._tick()
    assert( 245.37 == approx(s.car._x, .01) )


def test_register_keys_0():
    s = MovementSimulation(2)
    quit_event = pygame.event.Event(pygame.QUIT)
    assert( True == s._register_keys(quit_event) )


def test_register_keys_1():
    s = MovementSimulation(2)
    assert( 0 == s.car.drift_angle)
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_d})
    assert( False == s._register_keys(steer_right) )
    assert( 5 == s.rotation)

# other functions are tested in Base

def test_run():
    # test private functions instead
    Ellipsis