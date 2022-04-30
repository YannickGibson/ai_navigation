

from app.src.simulation.base import Simulation
from pytest import approx
import pygame


def test_set_spawn():
    s = Simulation(0)
    assert( (172, 363) == s.spawn_point )

    s = Simulation(1)
    assert( 31.35 == approx(s.spawn_deg, 0.01)) #direction of the game
    assert( (212, 343) == s.spawn_point )

def test_load_road():
    s = Simulation(0, False)
    assert( 2 == len(s.road))
    assert( 41 == len(s.road[0]))

    s = Simulation(1)
    assert( 2 == len(s.road))
    assert( 44 == len(s.road[0]))

def test_load_fitness():
    s = Simulation(0, False)
    assert( 32 == len(s.fitness_lines))
    assert( 2 == len(s.fitness_lines[0]))

    s = Simulation(1)
    assert( 43 == len(s.fitness_lines))
    assert( 2 == len(s.fitness_lines[0]))

def test_register_keys_0():
    s = Simulation(2)
    quit_event = pygame.event.Event(pygame.QUIT)
    assert( True == s._register_keys(quit_event) )

def test_register_keys_1():
    s = Simulation(2)
    assert( 0 == s.car.acc)
    run_forward_event = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_w})
    assert( False == s._register_keys(run_forward_event) )
    assert( 1 == s.car.acc)

def test_register_keys_2():
    s = Simulation(2)
    assert( 0 == s.car.acc)
    run_backwards_event = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_s})
    assert( False == s._register_keys(run_backwards_event) )
    assert( -1 == s.car.acc)

def test_register_keys_3():
    s = Simulation(2)
    assert( 0 == s.car.drift_angle)
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_d})
    assert( False == s._register_keys(steer_right) )
    assert( 5 == s.rotation)

def test_run():
    # method uses abstract method therefore we cannot test it directly
    Ellipsis