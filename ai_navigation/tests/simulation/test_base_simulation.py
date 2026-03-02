"""Unit tests for base Simulation class.

Tests cover:
- Spawn point calculation from fitness lines
- Road data loading
- Fitness checkpoint loading
- Keyboard input handling
- Window initialization
"""

import pygame
from pytest import approx

from ai_navigation.src.simulation.base_simulation import Simulation


def test_set_spawn() -> None:
    """Tests spawn point setting for different simulations."""
    # Arrange
    SPAWN_POINT_0 = (172, 363)
    SPAWN_POINT_1 = (212, 343)
    SPAWN_DEG_1 = 31.35

    # Act
    s0 = Simulation(0)
    spawn_point_0 = s0.spawn_point
    s1 = Simulation(1)
    spawn_deg_1 = s1.spawn_deg
    spawn_point_1 = s1.spawn_point

    # Assert
    assert spawn_point_0 == SPAWN_POINT_0
    assert approx(spawn_deg_1, 0.01) == SPAWN_DEG_1
    assert spawn_point_1 == SPAWN_POINT_1


def test_load_road() -> None:
    """Tests road loading for different simulations."""
    # Arrange
    ROAD_COUNT = 2
    ROAD_0_LENGTH = 41
    ROAD_1_LENGTH = 44

    # Act
    s0 = Simulation(0, False)
    road_0_count = len(s0.road)
    road_0_length = len(s0.road[0])
    s1 = Simulation(1)
    road_1_count = len(s1.road)
    road_1_length = len(s1.road[0])

    # Assert
    assert road_0_count == ROAD_COUNT
    assert road_0_length == ROAD_0_LENGTH
    assert road_1_count == ROAD_COUNT
    assert road_1_length == ROAD_1_LENGTH


def test_load_fitness() -> None:
    """Tests fitness lines loading for different simulations."""
    # Arrange
    FITNESS_LINES_0_COUNT = 32
    FITNESS_LINES_1_COUNT = 43
    FITNESS_LINE_DIMENSION = 2

    # Act
    s0 = Simulation(0, False)
    fitness_lines_0_count = len(s0.fitness_lines)
    fitness_line_0_dimension = len(s0.fitness_lines[0])
    s1 = Simulation(1)
    fitness_lines_1_count = len(s1.fitness_lines)
    fitness_line_1_dimension = len(s1.fitness_lines[0])

    # Assert
    assert fitness_lines_0_count == FITNESS_LINES_0_COUNT
    assert fitness_line_0_dimension == FITNESS_LINE_DIMENSION
    assert fitness_lines_1_count == FITNESS_LINES_1_COUNT
    assert fitness_line_1_dimension == FITNESS_LINE_DIMENSION


def test_register_keys_0() -> None:
    """Tests registering the quit event."""
    # Arrange
    s = Simulation(2)

    # Act
    quit_event = pygame.event.Event(pygame.QUIT)
    end_simulation = s._register_keys(quit_event)

    # Assert
    assert end_simulation


def test_register_keys_1() -> None:
    """Tests registering the forward acceleration key."""
    # Arrange
    s = Simulation(2)
    INITIAL_ACC = 0
    EXPECTED_ACC = 1

    # Act
    initial_acc = s.car.acc
    run_forward_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
    end_simulation = s._register_keys(run_forward_event)
    final_acc = s.car.acc

    # Assert
    assert initial_acc == INITIAL_ACC
    assert not end_simulation
    assert final_acc == EXPECTED_ACC


def test_register_keys_2() -> None:
    """Tests registering the backward acceleration key."""
    # Arrange
    s = Simulation(2)
    INITIAL_ACC = 0
    EXPECTED_ACC = -1

    # Act
    initial_acc = s.car.acc
    run_backwards_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_s})
    end_simulation = s._register_keys(run_backwards_event)
    final_acc = s.car.acc

    # Assert
    assert initial_acc == INITIAL_ACC
    assert not end_simulation
    assert final_acc == EXPECTED_ACC


def test_register_keys_3() -> None:
    """Tests registering the right steering key."""
    # Arrange
    s = Simulation(2)
    INITIAL_DRIFT_ANGLE = 0
    EXPECTED_ROTATION = 5

    # Act
    initial_drift_angle = s.car.drift_angle
    steer_right = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d})
    end_simulation = s._register_keys(steer_right)
    final_rotation = s.rotation

    # Assert
    assert initial_drift_angle == INITIAL_DRIFT_ANGLE
    assert not end_simulation
    assert final_rotation == EXPECTED_ROTATION


def test_run() -> None:
    """Tests that run method cannot be tested directly due to abstract method."""
    # Arrange
    # Method uses abstract method therefore we cannot test it directly

    # Act
    # No action performed

    # Assert
    # No assertions to make
    Ellipsis
