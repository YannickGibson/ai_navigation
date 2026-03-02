"""Base simulation module providing core functionality for car racing simulations.

This module defines the abstract Simulation class that handles common simulation tasks
including track loading, spawn point calculation, keyboard input handling, and the main
game loop. Concrete simulation types (training, movement) extend this base class.
"""

import math
import os
import pickle
from abc import abstractmethod
from typing import Never

import pygame

from ai_navigation.src.car import Car, sub
from ai_navigation.src.constants import (
    FITNESS_PICKLE_PATH,
    FRAMERATE,
    ROAD_PICKLE_PATH,
    ROTATION_RATE_FAST,
    ROTATION_RATE_NONE,
    WINDOW_POS_X,
    WINDOW_POS_Y,
)


class Simulation:
    """Abstract base class for all racing simulations.

    Provides core functionality shared across different simulation types including:
    - Track and fitness checkpoint loading
    - Spawn point calculation
    - Keyboard input handling
    - Main game loop structure
    - Pygame window management

    Subclasses must implement _draw() and _tick() methods to define
    specific rendering and update logic.

    Attributes:
        FRAMERATE (int): Target frames per second for simulation
        road_index (int): Index of the loaded track
        let_me_drive (bool): Whether manual car control is enabled
        road (list): Track boundary polygon data
        fitness_lines (list): Checkpoint lines for fitness scoring
        spawn_point (tuple): Starting position (x, y) for cars
        spawn_deg (float): Starting angle in degrees for cars

    """

    FRAMERATE = FRAMERATE

    def _load_road(self) -> None:
        """Load track boundary data from pickle file.

        Loads the track polygon vertices that define the racing surface.
        Cars must stay within these boundaries to avoid crashing.
        """
        # load road
        with open(ROAD_PICKLE_PATH.format(self.road_index), "rb") as f:
            self.road = pickle.load(f)

    def _load_fitness(self) -> None:
        """Load fitness checkpoint lines from pickle file.

        Checkpoints are invisible lines across the track that cars must cross
        to earn fitness points and track progress.
        """
        # load fitness lines
        with open(FITNESS_PICKLE_PATH.format(self.road_index), "rb") as f:
            self.fitness_lines = pickle.load(f)

    def __init__(self, road_index, let_me_drive=True) -> None:
        """Initialize the base simulation.

        Args:
            road_index (int): Index of the track to load
            let_me_drive (bool): Enable manual car control (default: True)

        """
        self.road_index = road_index
        self.let_me_drive = let_me_drive

        self.run_flag = False
        pygame.init()

        # Gives us the top bar
        os.environ["SDL_VIDEO_WINDOW_POS"] = f"{WINDOW_POS_X},{WINDOW_POS_Y}"

        self.current_w, self.current_h = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        )

        self._load_fitness()
        self._load_road()

        self._set_spawn()
        if self.let_me_drive:
            self.car = Car(*self.spawn_point, self.spawn_deg)
            self.rotation = 0

    def _set_spawn(self) -> None:
        """Calculate optimal spawn position and angle from fitness checkpoints.

        Determines the starting position by finding the midpoint between the first
        and last fitness checkpoint lines, and calculates the angle to face along
        the track direction.

        Sets:
            self.spawn_point (tuple): (x, y) coordinates for car spawn
            self.spawn_deg (float): Initial angle in degrees
        """
        diff1 = sub(*self.fitness_lines[0])
        diff2 = sub(*self.fitness_lines[-1])
        c1 = sub(
            self.fitness_lines[0][0],
            (diff1[0] / 2, diff1[1] / 2),
        )  # center of first fit line
        c2 = sub(
            self.fitness_lines[-1][0],
            (diff2[0] / 2, diff2[1] / 2),
        )  # center of last fit line
        diff3 = sub(c1, c2)
        spawnPoint = sub(c1, (diff3[0] / 2, diff3[1] / 2))  # middle of the two center

        self.spawn_point = (int(spawnPoint[0]), int(spawnPoint[1]))

        spawnRadians = math.atan2(c2[1] - c1[1], c2[0] - c1[0])
        self.spawn_deg = math.degrees(spawnRadians) - 90

    def _register_keys(self, event) -> bool:
        """Handle keyboard input events.

        Processes pygame events for:
        - ESC/Window Close: Exit simulation
        - WASD: Car acceleration and steering (if manual control enabled)

        Args:
            event (pygame.event.Event): Pygame event to process

        Returns:
            bool: True if simulation should exit, False otherwise

        """
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            self.run_flag = True
            pygame.quit()
            return True

        if self.let_me_drive:
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_a, pygame.K_d):
                    self.rotation = ROTATION_RATE_NONE
                elif event.key in (pygame.K_w, pygame.K_s):
                    self.car.acc = 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.rotation = -ROTATION_RATE_FAST
                elif event.key == pygame.K_d:
                    self.rotation = ROTATION_RATE_FAST
                elif event.key == pygame.K_w:
                    self.car.acc = 1
                elif event.key == pygame.K_s:
                    self.car.acc = -1

        return False

    def run(self):
        """Main game loop for the simulation.

        Runs at FRAMERATE fps, processing events and updating/rendering each frame.
        Continues until _register_keys() or _tick() signals exit.

        Returns:
            bool: Exit flag value from _register_keys() or _tick()

        """
        # Initialize window once (won't recreate if already exists)
        if not hasattr(self, "win") or self.win is None:
            self.win = pygame.display.set_mode((self.current_w, self.current_h))

        clock = pygame.time.Clock()
        while True:
            clock.tick(Simulation.FRAMERATE)
            for event in pygame.event.get():
                if self._register_keys(event):
                    return self.run_flag  # exited correctly

            if self._tick():
                return self.run_flag  # something has happened

            self._draw()

    @abstractmethod
    def _draw() -> Never:
        """Render the current simulation frame.

        Must be implemented by subclasses to define how the simulation
        state is visualized.

        Raises:
            NotImplementedError: If not implemented by subclass

        """
        msg = "Please Implement this method"
        raise NotImplementedError(msg)

    @abstractmethod
    def _tick() -> Never:
        """Update simulation state for one frame.

        Must be implemented by subclasses to define the simulation's
        update logic and determine when to exit.

        Returns:
            bool: True if simulation should exit, False to continue

        Raises:
            NotImplementedError: If not implemented by subclass

        """
        msg = "Please Implement this method"
        raise NotImplementedError(msg)
