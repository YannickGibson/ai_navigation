"""Manual car control simulation for testing physics and controls.

This module provides a simple simulation mode where users can manually drive
a car around the track to test the physics engine, controls, and collision detection.
Useful for debugging and demonstrating car behavior.
"""

import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from ai_navigation.src.car import add, normalize, sub
from ai_navigation.src.constants import (
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_WHITE,
    STAT_FONT,
    VISION_OFFSET_DISTANCE,
)
from ai_navigation.src.simulation.base_simulation import Simulation


class MovementSimulation(Simulation):
    """Manual driving simulation for single-player car control.

    Provides a simple mode where the user directly controls a single car using
    keyboard input. Displays visual debugging information including:
    - Car collision boundaries
    - Vision rays showing sensor distances
    - Current angle and drift statistics
    - Fitness checkpoint lines

    Background turns red when the car collides with track boundaries.
    """

    def __init__(self, road_index) -> None:
        """Initialize manual movement simulation.

        Args:
            road_index (int): Index of the track to load

        """
        super().__init__(road_index)

    def _draw(self) -> None:
        """Render the manual driving simulation frame.

        Draws:
        - Background (red if crashed, black if safe)
        - Track boundaries
        - Fitness checkpoint lines
        - Car collision polygon
        - Vision rays showing distances to track edges
        - Statistics (angle, drift angle)
        """
        # background
        if self.car.collides(self.road):
            self.win.fill(COLOR_RED)
        else:
            self.win.fill(COLOR_BLACK)

        # road
        pygame.draw.polygon(self.win, COLOR_WHITE, self.road[0] + self.road[1])

        # fitness lines
        for points in self.fitness_lines:
            pygame.draw.aaline(self.win, COLOR_GREEN, points[0], points[1], 5)

        pygame.draw.polygon(self.win, COLOR_BLUE, self.car.getVertices())  # collider

        # info
        text = STAT_FONT.render(
            f"Angle: {round(self.car.angle, 2):<6}",
            1,
            COLOR_WHITE,
        )
        self.win.blit(text, (self.current_w - 10 - text.get_width(), 10))
        text = STAT_FONT.render(
            f"Twirl: {round(self.car.drift_angle, 2):<6}",
            1,
            COLOR_WHITE,
        )
        self.win.blit(
            text, (self.current_w - 10 - text.get_width(), 10 + text.get_height())
        )

        # vision
        for p in self.car.get_vision(self.road):
            intersect_point = (int(p[0]), int(p[1]))
            diff = sub(intersect_point, self.car._center)
            offset_center = add(
                normalize(diff, scale=VISION_OFFSET_DISTANCE),
                self.car._center,
            )
            pygame.draw.aaline(self.win, COLOR_CYAN, offset_center, intersect_point)

            pygame.draw.circle(self.win, COLOR_BLUE, (int(p[0]), int(p[1])), 5)

        pygame.display.update()

    def _tick(self) -> None:
        """Update car position and rotation for manual control.

        Applies user input to rotate and move the car each frame.
        """
        self.car.rotate_by(self.rotation)
        self.car.move()
