"""Unit tests for Car movement and physics.

Tests cover:
- Forward and backward movement
- Rotation and drift mechanics
- Angle updates during movement
- Position changes over time
"""

from pytest import approx

from ai_navigation.src.car import Car, RotatingState


def test_move_0() -> None:
    """Tests car rotation and angle changes during forward movement."""
    # Arrange
    c = Car(0, 0, 0)
    EXPECTED_ANGLE_STEP1 = 0.54
    EXPECTED_ANGLE_STEP2 = 1.98
    EXPECTED_ANGLE_STEP3 = 4.24
    EXPECTED_ANGLE_STEP4 = 4.53

    # Act
    c.rotate_by(5)
    c.acc = 1
    c.move()
    angle_step1 = c.angle
    c.rotate_by(5)
    c.move()
    angle_step2 = c.angle
    c.rotate_by(5)
    c.move()
    angle_step3 = c.angle
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    angle_step4 = c.angle

    # Assert
    assert approx(angle_step1, 0.01) == EXPECTED_ANGLE_STEP1
    assert approx(angle_step2, 0.01) == EXPECTED_ANGLE_STEP2
    assert approx(angle_step3, 0.01) == EXPECTED_ANGLE_STEP3
    assert approx(angle_step4, 0.01) == EXPECTED_ANGLE_STEP4


def test_move_1() -> None:
    """Tests car rotation during backward movement."""
    # Arrange
    c = Car(10, 100, 60)
    EXPECTED_ANGLE_STEP1 = 59.46
    EXPECTED_ANGLE_STEP2 = 58.01
    EXPECTED_ANGLE_STEP3 = 56.80
    EXPECTED_ANGLE_STEP4 = 56.95

    # Act
    c.rotate_by(5)
    c.acc = -1
    c.move()
    angle_step1 = c.angle
    c.rotate_by(5)
    c.move()
    angle_step2 = c.angle
    c.rotate_by(0)
    c.move()
    angle_step3 = c.angle
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    angle_step4 = c.angle

    # Assert
    assert approx(angle_step1, 0.01) == EXPECTED_ANGLE_STEP1
    assert approx(angle_step2, 0.01) == EXPECTED_ANGLE_STEP2
    assert approx(angle_step3, 0.01) == EXPECTED_ANGLE_STEP3
    assert approx(angle_step4, 0.01) == EXPECTED_ANGLE_STEP4


def test_move_2() -> None:
    """Tests drift angle and rotating state during movement."""
    # Arrange
    c = Car(10, 100, 60)
    EXPECTED_DRIFT_ANGLE = 1.45
    EXPECTED_ANGLE_STEP3 = 56.80
    EXPECTED_ANGLE_STEP4 = 56.95

    # Act
    c.rotate_by(5)
    c.acc = -1
    c.move()
    drift_angle = c.drift_angle
    c.rotate_by(5)
    c.move()
    rotating_state = c.rotating_state
    c.rotate_by(0)
    c.move()
    angle_step3 = c.angle
    c.acc = 0
    c.rotate_by(-5)
    c.move()
    angle_step4 = c.angle

    # Assert
    assert approx(drift_angle, 0.01) == EXPECTED_DRIFT_ANGLE
    assert RotatingState.calm == rotating_state
    assert approx(angle_step3, 0.01) == EXPECTED_ANGLE_STEP3
    assert approx(angle_step4, 0.01) == EXPECTED_ANGLE_STEP4


def test_move_3() -> None:
    """Tests final angle after sequence of movements."""
    # Arrange
    c = Car(10, 100, 60)
    EXPECTED_FINAL_ANGLE = 56.95

    # Act
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
    final_angle = c.angle

    # Assert
    assert approx(final_angle, 0.01) == EXPECTED_FINAL_ANGLE
