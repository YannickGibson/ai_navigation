"""Training simulation module for AI-driven car navigation using NEAT algorithm.

This module implements a genetic algorithm-based training system where neural networks
learn to navigate cars through race tracks. It uses the NEAT (NeuroEvolution of Augmenting
Topologies) algorithm to evolve car controllers over generations.
"""

import os
import pickle

import neat
import pygame

from ai_navigation.src.car import Car
from ai_navigation.src.constants import (
    AI_ACCELERATION_THRESHOLD,
    AI_ROTATION_THRESHOLD_HIGH,
    AI_ROTATION_THRESHOLD_LOW,
    COLOR_BLACK,
    COLOR_BLUE,
    COLOR_BLUE_DARK,
    COLOR_CROSSED,
    COLOR_CYAN,
    COLOR_LIGHT_PINK,
    COLOR_MAGENTA,
    COLOR_NOT_CROSSED,
    COLOR_PURPLE,
    COLOR_RED,
    COLOR_RED_DARK,
    COLOR_WHITE,
    CONFIG_PATH,
    DEFAULT_MAX_FRAMES_ELAPSED,
    DEFAULT_NO_PROGRESS_FRAMES_ELAPSED,
    FITNESS_LOOKBACK_DISTANCE,
    FITNESS_PENALTY_BACKWARD,
    FITNESS_REWARD_FORWARD,
    GENOME_PICKLE_PATH,
    ROTATION_RATE_FAST,
    ROTATION_RATE_NONE,
    STAT_FONT,
)
from ai_navigation.src.simulation.base_simulation import Simulation


class ExitSimulationException(BaseException):
    """Custom exception to gracefully exit the training simulation loop."""


class TrainSimulation(Simulation):
    """AI training simulation using NEAT genetic algorithm for car navigation.

    This class manages the evolutionary training process where neural networks learn
    to control cars through race tracks. Each generation spawns multiple cars controlled
    by evolved neural networks, and the best performers pass their genes to the next
    generation.

    Attributes:
        show_active_fitness_lines (bool): Display fitness checkpoints for each car
        show_car_vision (bool): Display vision rays from cars to track boundaries
        show_all_fitness_lines (bool): Display all fitness checkpoints on track
        show_parent (bool): Highlight the best performing car from previous generation
        save_best_genome (bool): Save the best genome to disk after training
        gen_num (int): Current generation number
        champion_not_beaten_n (int): Generations since champion was surpassed
        population (neat.Population): NEAT population manager
        prev_best_genome (neat.DefaultGenome): Best genome from previous generation

    """

    def __init__(
        self,
        road_index=0,
        show_active_fitness_lines=True,
        show_car_vision=False,
        show_all_fitness_lines=True,
        show_parent=True,
        save_best_genome=False,
        reverse_fitness_lines=False,
        let_me_drive=False,
        max_frames_elapsed=DEFAULT_MAX_FRAMES_ELAPSED,
        no_progress_frames_elapsed=DEFAULT_NO_PROGRESS_FRAMES_ELAPSED,
    ) -> None:
        """Initialize the training simulation with configuration parameters.

        Args:
            road_index (int): Index of the track to load (0-N)
            show_active_fitness_lines (bool): Show current fitness checkpoint for each car
            show_car_vision (bool): Display vision rays showing car's sensors
            show_all_fitness_lines (bool): Display all fitness checkpoints on track
            show_parent (bool): Highlight the champion from previous generation
            save_best_genome (bool): Save best genome to file after training
            reverse_fitness_lines (bool): Reverse checkpoint order (for backwards racing)
            let_me_drive (bool): Allow manual car control alongside AI
            max_frames_elapsed (int): Maximum frames before forcing new generation
            no_progress_frames_elapsed (int): Frames without progress before new generation

        """
        self.show_active_fitness_lines = show_active_fitness_lines
        self.show_car_vision = show_car_vision
        self.show_all_fitness_lines = show_all_fitness_lines
        self.show_parent = show_parent
        self.save_best_genome = save_best_genome
        self.gen_num = 0
        self.rotation = 0
        self.champion_not_beaten_n = 0
        self.population = None
        self.prev_best_genome = None
        self.reverse_fitness_lines = reverse_fitness_lines
        self.let_me_drive = let_me_drive
        self.max_frames_elapsed = max_frames_elapsed
        self.no_progress_frames_elapsed = no_progress_frames_elapsed

        self.no_fitness_crossed_for = 0
        self.fitness_crossed = False

        super().__init__(road_index, self.let_me_drive)

    def _load_fitness(self) -> None:
        """Load fitness checkpoint lines from file and optionally reverse them.

        Extends parent method to support reversed checkpoint order for alternative
        racing directions or training scenarios.
        """
        super()._load_fitness()
        if self.reverse_fitness_lines:
            self.fitness_lines = list(reversed(self.fitness_lines))

    def draw_agent_cars(self):
        """Draw AI-controlled cars with optional fitness lines and vision.

        Renders all active AI cars and their visual debugging aids including:
        - Current and previous fitness checkpoints for each car
        - Vision rays showing sensor distances to track boundaries
        - Identification of the best performing car (champion)

        Returns:
            Car or None: The best genome's car to be highlighted, or None

        """
        best_genome_car = None
        for i, car in enumerate(self.cars):
            if self.show_active_fitness_lines:
                # Fitness lines for each car
                pygame.draw.line(
                    self.win,
                    COLOR_CYAN,
                    self.fitness_lines[self.fit_indexes[i]][0],
                    self.fitness_lines[self.fit_indexes[i]][1],
                    2,
                )

                pygame.draw.line(
                    self.win,
                    COLOR_RED,
                    self.fitness_lines[self.fit_indexes[i] - FITNESS_LOOKBACK_DISTANCE][
                        0
                    ],
                    self.fitness_lines[self.fit_indexes[i] - FITNESS_LOOKBACK_DISTANCE][
                        1
                    ],
                )

            if self.show_car_vision and hasattr(car, "_cached_vision"):
                # Use cached vision from _think() instead of recalculating
                for p in car._cached_vision:
                    pygame.draw.line(
                        self.win,
                        COLOR_MAGENTA,
                        car.center,
                        (int(p[0]), int(p[1])),
                        1,
                    )
                    pygame.draw.circle(
                        self.win,
                        COLOR_BLUE_DARK,
                        (int(p[0]), int(p[1])),
                        3,
                    )

            if self.show_parent and self.population.best_genome == self.ge[i]:
                best_genome_car = car
            else:
                car.draw(self.win)

        return best_genome_car

    def draw_user_car(self) -> None:
        """Draw user-controlled car with optional vision debugging.

        Renders the manually controlled car (if enabled) with vision rays
        showing sensor distances. The car is highlighted in blue to distinguish
        it from AI-controlled cars.
        """
        if self.show_car_vision:
            for p in self.car.get_vision(self.road):
                pygame.draw.aaline(
                    self.win,
                    COLOR_MAGENTA,
                    self.car.center,
                    (int(p[0]), int(p[1])),
                    1,
                )
                pygame.draw.circle(
                    self.win,
                    COLOR_BLUE_DARK,
                    (int(p[0]), int(p[1])),
                    3,
                )
        self.car.draw_shadow(self.win, COLOR_BLUE)

    def _draw(self) -> None:
        """Render the complete simulation frame.

        Draws all visual elements in proper layering order:
        1. Background (red if user car crashed, black otherwise)
        2. Race track polygon
        3. AI-controlled cars
        4. User-controlled car (if enabled)
        5. Statistics text (car count, frame count, generation number)
        6. All fitness checkpoint lines (if enabled)
        7. Crossed fitness lines (highlighted)
        8. Champion car highlight (if applicable)

        Updates the display after all elements are drawn.
        """
        if self.let_me_drive and self.car.collides(self.road):
            self.win.fill(COLOR_RED_DARK)
        else:
            self.win.fill(COLOR_BLACK)

        # Road
        pygame.draw.polygon(
            self.win,
            COLOR_PURPLE,
            [self.road[1][0], self.road[0][0]] + self.road[0] + self.road[1],
        )

        # Cars
        best_genome_car = self.draw_agent_cars()

        if self.let_me_drive:
            self.draw_user_car()

        # Info
        text = STAT_FONT.render(f"Car count: {len(self.cars):>4}", 1, COLOR_WHITE)
        self.win.blit(text, (self.current_w - 10 - text.get_width(), 10))
        text = STAT_FONT.render(f"Frame: {self.frames_passed:>4}", 1, COLOR_WHITE)
        self.win.blit(
            text,
            (self.current_w - 10 - text.get_width(), text.get_height() + 20),
        )
        text = STAT_FONT.render("Gen: " + str(self.gen_num), 1, COLOR_WHITE)
        self.win.blit(text, (10, 10))

        if self.show_all_fitness_lines:
            # Fitness lines
            pygame.draw.line(
                self.win,
                COLOR_RED,
                self.fitness_lines[0][0],
                self.fitness_lines[0][1],
                5,
            )
            for points in self.fitness_lines[1:]:
                pygame.draw.line(self.win, COLOR_NOT_CROSSED, points[0], points[1], 5)

        # Draw crossed fitness lines (after everything else so they're visible)
        if hasattr(self, "_crossed_lines"):
            for line in self._crossed_lines:
                # Don't overwrite the red start line
                if line != self.fitness_lines[0]:
                    pygame.draw.line(self.win, COLOR_CROSSED, *line, 5)

        if best_genome_car is not None:
            best_genome_car.draw_shadow(self.win, COLOR_LIGHT_PINK)

        pygame.display.update()

    def _iterate_ai(self, genomes, config) -> None:
        """Execute one generation of the genetic algorithm.

        Called by NEAT for each generation. Initializes cars with evolved neural
        networks, runs the simulation until all cars crash or time limit reached,
        and tracks the best performing genomes.

        Args:
            genomes (list): List of (id, genome) tuples from NEAT
            config (neat.Config): NEAT configuration object

        Raises:
            ExitSimulationException: If user requests simulation exit

        """
        self.gen_num += 1
        self.frames_passed = 0

        # Reset crossed fitness lines for new generation
        self._crossed_lines = []

        if (
            self.population.best_genome is not None
            and self.population.best_genome == self.prev_best_genome
        ):
            self.champion_not_beaten_n += 1
        else:
            self.champion_not_beaten_n = 0
            self.prev_best_genome = self.population.best_genome

        self.nets = []
        self.ge = []
        self.cars = []

        for _, g in genomes:  # (id, obj)
            net = neat.nn.FeedForwardNetwork.create(g, config)  # Input, output
            self.nets.append(net)
            c = Car(*self.spawn_point, self.spawn_deg)
            self.cars.append(c)
            g.fitness = 0
            self.ge.append(g)

        self.fit_indexes = [
            0 for _ in self.cars
        ]  # Index of last fitnessLine they crossed

        if super().run():
            raise ExitSimulationException

    def _register_keys(self, event) -> bool:
        """Handle training-specific keyboard events.

        Extends parent key handling to add DELETE key for stopping the current
        generation and moving to the next one.

        Args:
            event (pygame.event.Event): Pygame event to process

        Returns:
            bool: True if simulation should exit, False otherwise

        """
        if super()._register_keys(event):
            return True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            self.run_flag = False
            return True

        return False

    def _think(self, car: Car, i: int) -> None:
        """Process AI decision-making for a single car.

        Uses the car's neural network to determine actions based on sensor inputs:
        - Vision distances to track boundaries (8 directions)
        - Current drift angle
        - Current speed

        The network outputs control decisions for acceleration and steering,
        then updates the car's fitness score based on checkpoint crossings.

        Args:
            car (Car): The car to control
            i (int): Index of the car in the cars list

        """
        vision = car.vision_distance(self.road)
        # Cache vision points for drawing (avoid recalculating)
        car._cached_vision = car.get_vision(self.road)
        for _i in range(len(vision)):
            vision[_i] = vision[_i] / car.sight

        front_acc, back_acc, rot = self.nets[i].activate(
            [*vision, car.drift_angle / 360, car.speed],
        )  # Drifting
        if rot > AI_ROTATION_THRESHOLD_HIGH:
            car.rotate_by(ROTATION_RATE_FAST)
        elif rot < AI_ROTATION_THRESHOLD_LOW:
            car.rotate_by(-ROTATION_RATE_FAST)
        else:
            car.rotate_by(ROTATION_RATE_NONE)

        if front_acc > AI_ACCELERATION_THRESHOLD:
            car.acc = 1
        elif back_acc > AI_ACCELERATION_THRESHOLD:
            car.acc = -1
        else:
            car.acc = 0

        car.move()

        front_line = self.fitness_lines[
            self.fit_indexes[i]
        ]  # Check if crossing fitness_lines in direction of the race
        back_line = self.fitness_lines[
            self.fit_indexes[i] - FITNESS_LOOKBACK_DISTANCE
        ]  # Check if going back
        if car.collide_fitness(front_line[0], front_line[1]):
            self.fitness_crossed = True
            self.ge[i].fitness += FITNESS_REWARD_FORWARD
            # Store fitness line to draw in _draw() instead
            if not hasattr(self, "_crossed_lines"):
                self._crossed_lines = []
            self._crossed_lines.append(front_line)
            self.fit_indexes[i] += 1
        elif car.collide_fitness(back_line[0], back_line[1]):
            self.ge[i].fitness -= FITNESS_PENALTY_BACKWARD
            self.fit_indexes[i] -= 1

        self.fit_indexes[i] %= len(self.fitness_lines)  # Put it back to the world of Zn

    def _tick(self) -> bool:
        """Update simulation state for one frame.

        Processes all cars in the current generation:
        - Moves user car if manual control enabled
        - Checks each AI car for collisions with track boundaries
        - Executes AI decision-making for surviving cars
        - Removes crashed cars from simulation
        - Monitors progress to determine if generation should end

        Returns:
            bool: True if new generation should start, False to continue current generation

        """
        if self.let_me_drive:
            self.car.rotate_by(self.rotation)
            self.car.move()
        self.fitness_crossed = False

        # Process all cars and mark survivors
        surviving_indices = []
        for i, car in enumerate(self.cars):
            if car.collides(self.road):
                continue

            self._think(car, i)
            surviving_indices.append(i)

        # Rebuild lists with only surviving cars
        self.cars = [self.cars[i] for i in surviving_indices]
        self.nets = [self.nets[i] for i in surviving_indices]
        self.ge = [self.ge[i] for i in surviving_indices]
        self.fit_indexes = [self.fit_indexes[i] for i in surviving_indices]

        if self.fitness_crossed:
            self.no_fitness_crossed_for = 0
        else:
            self.no_fitness_crossed_for += 1
            if self.no_fitness_crossed_for > self.no_progress_frames_elapsed:
                self.no_fitness_crossed_for = 0
                return True  # New gen

        if len(self.cars) <= 0 or self.frames_passed > self.max_frames_elapsed:
            return True  # New gen

        self.frames_passed += 1
        return False

    def run(self, n=10000) -> bool:
        """Run the genetic algorithm training for specified number of generations.

        Configures NEAT and starts the evolutionary training process. The simulation
        continues until the maximum number of generations is reached or the user
        manually exits.

        Args:
            n (int): Maximum number of generations to evolve (default: 10000)

        Returns:
            bool: False when training completes normally

        """
        config_path = CONFIG_PATH

        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )
        p = neat.Population(config)
        self.population = p

        try:
            p.run(self._iterate_ai, n=n)  # Num of generations
        except ExitSimulationException:
            pass

        if self.prev_best_genome:
            self.save_genome(self.prev_best_genome)
        return False

    def save_genome(self, genome) -> None:
        """Save a genome to disk for later use.

        Automatically finds the next available filename (genome0.pickle, genome1.pickle, etc.)
        to avoid overwriting existing saved genomes.

        Args:
            genome (neat.DefaultGenome): The genome to save

        """
        i = 0
        while os.path.exists(GENOME_PICKLE_PATH.format(i)):
            i += 1
        with open(GENOME_PICKLE_PATH.format(i), "wb") as f:
            pickle.dump(genome, f)
