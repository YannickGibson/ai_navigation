

from app.src.car.car import Car
from app.src.simulation.ai import AiSimulation
from pytest import ExceptionInfo, approx, fixture
import pygame
import pickle
import os
import pytest
from app.src.simulation.base import Simulation

@pytest.fixture
def sample_genome():
    with open("app\\utils\\pickles\\genomes\\genome0.pickle","rb") as f:
        return pickle.load(f)

class FakeNeuralNet():
    def activate(self, x):
        return 1, 1, 1
conf = {
        "road_index": 2,
        "show_active_fitness_lines": True,
        "show_car_vision": True,
        "show_all_fitness_lines": True,
        "show_parent": True,
        "save_best_genome": False,
        "reverse_fitness_lines": True,
        "let_me_drive": True,
        "max_frames_elapsed": 1000,
        "no_progress_frames_elapsed": 50

    }

def test_load_fitness_reversed():
    s = Simulation(2)
    ai = AiSimulation(**conf)
    assert( list(reversed(s.fitness_lines)) == ai.fitness_lines)

def test_register_keys_0():
    ai = AiSimulation(**conf)
    assert( 0 == ai.car.drift_angle)
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_d})
    assert( False == ai._register_keys(steer_right) )
    assert( 5 == ai.rotation)

def test_register_keys_1():
    ai = AiSimulation(**conf)
    assert( 0 == ai.car.drift_angle)
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_a})
    assert( False == ai._register_keys(steer_right) )
    assert( -5 == ai.rotation)
    
def test_register_keys_2():
    ai = AiSimulation(**conf)
    assert( 0 == ai.car.drift_angle)
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key":pygame.K_DELETE})
    assert( True == ai._register_keys(steer_right) )


def test_save_genome():
    ai = AiSimulation(**conf)

    test_genome = sample_genome

    assert(test_genome is not None )

    i = 0
    while os.path.exists("app\\utils\\pickles\\genomes\\genome{}.pickle".format(i)):
        i += 1
    ai.save_genome(test_genome)
    assert ( True == os.path.exists("app\\utils\\pickles\\genomes\\genome{}.pickle".format(i)))
    os.remove("app\\utils\\pickles\\genomes\\genome{}.pickle".format(i)) 
        

def test_tick():

    ai = AiSimulation(**conf)

    ai.nets = []
    ai.ge = []
    ai.cars = []
    assert( True == ai._tick())
    test_genome = sample_genome
    ai.nets = [FakeNeuralNet()]
    ai.ge = [test_genome]
    ai.cars = [Car(0, 0, 0)]
    ai.frames_passed = 0
    ai.fit_indexes = [0]
    assert( False == ai._tick())

def test_think():
    ai = AiSimulation(**conf)

    ai.nets = []
    ai.ge = []
    ai.cars = []
    assert( True == ai._tick())
    test_genome = sample_genome
    ai.nets = [FakeNeuralNet()]
    ai.ge = [test_genome]
    ai.cars = [Car(0,0,0)]
    ai.frames_passed = 0
    ai.fit_indexes = [0]
    for _ in range(100):
        assert( None == ai._think(ai.cars[0], 0))
    assert( 12.95 == approx(ai.cars[0]._x, .01))
    for _ in range(100):
        assert( None == ai._think(ai.cars[0], 0))
    assert(  59.36 == approx(ai.cars[0]._x, .01) )

# _iterate_ai is only calling neat method, not much to test there
# overrided run method is only running the simulation which we have simulated internally while testing _think and _tick methods
# other methods are tested in Base and MovementSimulation

def test_run():
    # test private functions instead
    Ellipsis