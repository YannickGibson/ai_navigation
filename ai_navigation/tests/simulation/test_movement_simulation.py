"""Unit tests for MovementSimulation class.

Tests cover:
- Manual car control (forward, backward, turning)
- Movement physics accuracy
- Keyboard input handling
- Position and angle updates
"""

import pygame
from pytest import approx

from ai_navigation.src.simulation.movement_simulation import MovementSimulation


def test_movement_0() -> None:
    """Tests basic forward movement simulation."""
    # Arrange
    s = MovementSimulation(0)
    INITIAL_X = 168
    EXPECTED_FINAL_X = 171.92
    TICK_COUNT = 10

    # Act
    initial_x = s.car._x
    go_forward = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
    end_simulation = s._register_keys(go_forward)
    for _ in range(TICK_COUNT):
        s._tick()
    final_x = s.car._x

    # Assert
    assert initial_x == INITIAL_X
    assert not end_simulation
    assert approx(final_x, 0.01) == EXPECTED_FINAL_X


def test_movement_forward_backward() -> None:
    """Tests forward and backward movement sequence."""
    # Arrange
    s = MovementSimulation(1)
    INITIAL_ANGLE = 31.35
    INITIAL_X = 208
    EXPECTED_X_AFTER_FORWARD = 224.56
    EXPECTED_X_AFTER_BACKWARD = 88.59
    FORWARD_TICK_COUNT = 10
    BACKWARD_TICK_COUNT = 50

    # Act
    initial_angle = s.car.angle
    initial_x = s.car._x
    go_forward = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
    end_simulation_1 = s._register_keys(go_forward)
    for _ in range(FORWARD_TICK_COUNT):
        s._tick()
    x_after_forward = s.car._x
    stop_forward = pygame.event.Event(pygame.KEYUP, {"key": pygame.K_w})
    end_simulation_2 = s._register_keys(stop_forward)
    go_backward = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_s})
    end_simulation_3 = s._register_keys(go_backward)
    for _ in range(BACKWARD_TICK_COUNT):
        s._tick()
    x_after_backward = s.car._x

    # Assert
    assert approx(initial_angle, 0.01) == INITIAL_ANGLE
    assert initial_x == INITIAL_X
    assert not end_simulation_1
    assert approx(x_after_forward, 0.01) == EXPECTED_X_AFTER_FORWARD
    assert not end_simulation_2
    assert not end_simulation_3
    assert approx(x_after_backward, 0.01) == EXPECTED_X_AFTER_BACKWARD


def test_inertia() -> None:
    """Tests car inertia after stopping forward movement."""
    # Arrange
    s = MovementSimulation(1)
    INITIAL_ANGLE = 31.35
    INITIAL_X = 208
    EXPECTED_X_AFTER_FORWARD = 224.56
    EXPECTED_X_AFTER_INERTIA = 245.37
    FORWARD_TICK_COUNT = 10
    INERTIA_TICK_COUNT = 100

    # Act
    initial_angle = s.car.angle
    initial_x = s.car._x
    go_forward = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_w})
    end_simulation_1 = s._register_keys(go_forward)
    for _ in range(FORWARD_TICK_COUNT):
        s._tick()
    x_after_forward = s.car._x
    stop_forward = pygame.event.Event(pygame.KEYUP, {"key": pygame.K_w})
    end_simulation_2 = s._register_keys(stop_forward)
    for _ in range(INERTIA_TICK_COUNT):
        s._tick()
    x_after_inertia = s.car._x

    # Assert
    assert approx(initial_angle, 0.01) == INITIAL_ANGLE
    assert initial_x == INITIAL_X
    assert not end_simulation_1
    assert approx(x_after_forward, 0.01) == EXPECTED_X_AFTER_FORWARD
    assert not end_simulation_2
    assert approx(x_after_inertia, 0.01) == EXPECTED_X_AFTER_INERTIA


def test_end_game() -> None:
    """Tests registering the quit event."""
    # Arrange
    s = MovementSimulation(2)

    # Act
    quit_event = pygame.event.Event(pygame.QUIT)
    end_simulation = s._register_keys(quit_event)

    # Assert
    assert end_simulation


def test_turn_right() -> None:
    """Tests registering the turn key."""
    # Arrange
    s = MovementSimulation(2)
    DRIFT_VALUE = 0
    END_ROTATION = 5

    # Act
    init_drift_value = s.car.drift_angle
    steer_right_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_d})
    end_simulation = s._register_keys(steer_right_event)

    # Assert
    assert init_drift_value == DRIFT_VALUE
    assert not end_simulation
    assert s.rotation == END_ROTATION
