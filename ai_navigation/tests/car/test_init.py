"""Unit tests for Car initialization and rendering.

Tests cover:
- Car initialization with correct default values
- Drawing methods (normal and shadow)
- Property access
"""

import pygame

from ai_navigation.src.car import Car


def test_init() -> None:
    """Tests car initialization with default values."""
    # Arrange
    INITIAL_ACC = 0
    EXPECTED_SIGHT = 400
    INITIAL_ANGLE = 0

    # Act
    c = Car(0, 0, 0)

    # Assert
    assert c.acc == INITIAL_ACC
    assert c.sight == EXPECTED_SIGHT
    assert c.angle == INITIAL_ANGLE
    assert c.center is None


def test_draw_shadow() -> None:
    """Test car shadow rendering with color tint."""
    c = Car(0, 0, 0)
    win = pygame.display.set_mode((100, 100), flags=pygame.HIDDEN)
    assert win.get_at((0, 0)) == (0, 0, 0, 255)
    c.draw_shadow(win, [255, 0, 255])
    assert win.get_at((1, 1)) == (255, 0, 255, 255)


def test_draw() -> None:
    """Test normal car rendering."""
    c = Car(0, 0, 0)
    win = pygame.display.set_mode((100, 100), flags=pygame.HIDDEN)
    assert win.get_at((0, 0)) == (0, 0, 0, 255)
    c.draw(win)
    assert win.get_at((1, 1)) == (255, 255, 255, 255)
