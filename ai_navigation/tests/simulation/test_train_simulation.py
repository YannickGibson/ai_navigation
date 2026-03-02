"""Unit tests for TrainSimulation class.

Tests cover:
- Fitness line loading and reversal
- Keyboard input handling
- Genome saving functionality
- AI thinking and car control
- Generation lifecycle (_tick method)
"""

import os
import pickle

import pygame
import pytest
from pytest import approx

from ai_navigation.src.car import Car
from ai_navigation.src.simulation.base_simulation import Simulation
from ai_navigation.src.simulation.train_simulation import TrainSimulation


@pytest.fixture
def sample_genome():
    """Load a sample genome from disk for testing.

    Returns:
        neat.DefaultGenome: A pre-trained genome for testing AI behavior

    """
    with open("ai_navigation/data/pickles/genomes/genome0.pickle", "rb") as f:
        return pickle.load(f)


class FakeNeuralNet:
    """Mock neural network that always returns full activation.

    Used for testing car control without running actual NEAT evolution.
    """

    def activate(self, x):
        """Return constant outputs for all inputs.

        Args:
            x: Input array (ignored)

        Returns:
            tuple: (1, 1, 1) representing full forward, full backward, full right

        """
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
    "no_progress_frames_elapsed": 50,
}


def test_load_fitness_reversed() -> None:
    """Test that TrainSimulation correctly reverses fitness lines when configured."""
    s = Simulation(2)
    ai = TrainSimulation(**conf)
    assert list(reversed(s.fitness_lines)) == ai.fitness_lines


def test_register_keys_0() -> None:
    """Tests right steering key registration."""
    # Arrange
    ai = TrainSimulation(**conf)
    INITIAL_DRIFT_ANGLE = 0
    EXPECTED_ROTATION = 5

    # Act
    initial_drift = ai.car.drift_angle
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d})
    end_simulation = ai._register_keys(steer_right)
    final_rotation = ai.rotation

    # Assert
    assert initial_drift == INITIAL_DRIFT_ANGLE
    assert not end_simulation
    assert final_rotation == EXPECTED_ROTATION


def test_register_keys_1() -> None:
    """Tests left steering key registration."""
    # Arrange
    ai = TrainSimulation(**conf)
    INITIAL_DRIFT_ANGLE = 0
    EXPECTED_ROTATION = -5

    # Act
    initial_drift = ai.car.drift_angle
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
    end_simulation = ai._register_keys(steer_right)
    final_rotation = ai.rotation

    # Assert
    assert initial_drift == INITIAL_DRIFT_ANGLE
    assert not end_simulation
    assert final_rotation == EXPECTED_ROTATION


def test_register_keys_2() -> None:
    """Test DELETE key handling to end current generation."""
    ai = TrainSimulation(**conf)
    assert ai.car.drift_angle == 0
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_DELETE})
    assert ai._register_keys(steer_right)


def test_save_genome(sample_genome) -> None:
    """Test genome saving to disk with automatic filename generation."""
    ai = TrainSimulation(**conf)

    test_genome = sample_genome

    assert test_genome is not None

    i = 0
    while os.path.exists(
        f"ai_navigation/data/pickles/genomes/genome{i}.pickle",
    ):
        i += 1
    ai.save_genome(test_genome)
    assert os.path.exists(
        f"ai_navigation/data/pickles/genomes/genome{i}.pickle",
    )
    os.remove(f"ai_navigation/data/pickles/genomes/genome{i}.pickle")


def test_tick() -> None:
    """Test _tick method behavior with and without cars."""
    ai = TrainSimulation(**conf)

    ai.nets = []
    ai.ge = []
    ai.cars = []
    assert ai._tick()
    test_genome = sample_genome
    ai.nets = [FakeNeuralNet()]
    ai.ge = [test_genome]
    ai.cars = [Car(0, 0, 0)]
    ai.frames_passed = 0
    ai.fit_indexes = [0]
    assert not ai._tick()


def test_think() -> None:
    """Tests AI think method with car movement."""
    # Arrange
    ai = TrainSimulation(**conf)
    test_genome = sample_genome
    EXPECTED_X_AFTER_100 = 12.95
    EXPECTED_X_AFTER_200 = 59.36
    ITERATIONS = 100

    # Act
    ai.nets = []
    ai.ge = []
    ai.cars = []
    tick_result = ai._tick()

    ai.nets = [FakeNeuralNet()]
    ai.ge = [test_genome]
    ai.cars = [Car(0, 0, 0)]
    ai.frames_passed = 0
    ai.fit_indexes = [0]

    for _ in range(ITERATIONS):
        ai._think(ai.cars[0], 0)
    x_after_100 = ai.cars[0]._x

    for _ in range(ITERATIONS):
        ai._think(ai.cars[0], 0)
    x_after_200 = ai.cars[0]._x

    # Assert
    assert tick_result
    assert approx(x_after_100, 0.01) == EXPECTED_X_AFTER_100
    assert approx(x_after_200, 0.01) == EXPECTED_X_AFTER_200
