"""AI Navigation package for training neural networks to drive racing cars.

This package provides simulation environments for training and testing AI-controlled
cars using the NEAT genetic algorithm. Cars learn to navigate race tracks by evolving
neural networks that process vision sensors and control steering/acceleration.

Main classes:
    TrainSimulation: AI training environment using NEAT evolution
    MovementSimulation: Manual car control for testing and demonstration

Exports these classes for convenient import:
    from ai_navigation import TrainSimulation, MovementSimulation
"""

import os

from .src.simulation.movement_simulation import MovementSimulation
from .src.simulation.train_simulation import TrainSimulation

# Exposes members when `from package import import` runs
__all__ = ["MovementSimulation", "TrainSimulation"]

# Hide PyGame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
