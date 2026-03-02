"""Constants used throughout the AI navigation simulation.

This module defines all configuration constants for the racing simulation including:
- Car physics parameters (speed, acceleration, drift)
- AI control thresholds and behavior
- Visual rendering constants (colors, fonts)
- File paths for data storage
- Training simulation parameters
- Fitness scoring values

All values are tuned for realistic racing behavior and effective AI training.
"""

import pygame

# Image constants
CAR_IMG = pygame.image.load("ai_navigation/data/img/car.png")
GHOST_IMG = pygame.image.load("ai_navigation/data/img/ball.png")
IMG = GHOST_IMG

# Car physics constants
MAX_SPEED = 0.5
ACCELERATION_RATE = 0.8
VELOCITY_DECAY = 0.79
DRIFT_DECAY = 0.967
VELOCITY_AIR_RESISTANCE = 0.89
SPEED_DECAY = 0.6
DRIFT_LERP_SPEED = 0.3
MAX_DRIFT_ANGLE = 5
DRIFT_INFLUENCE = 4.5
ANGLE_RESET_THRESHOLD = 360
MAX_SPEED_THRESHOLD = 10
MIN_SPEED_THRESHOLD = 0.01

# Car vision constants
DEFAULT_SIGHT_DISTANCE = 400

# Car fitness constants
DEFAULT_FIT_DISTANCE_OFFSET = None  # Will be set to car height

# Simulation constants
FRAMERATE = 60

# Path constants
DATA_PATH = "ai_navigation/data/"
ROAD_PICKLE_PATH = "ai_navigation/data/pickles/roads/road{}.pickle"
FITNESS_PICKLE_PATH = "ai_navigation/data/pickles/fitness/fitnessLines{}.pickle"
GENOME_PICKLE_PATH = "ai_navigation/data/pickles/genomes/genome{}.pickle"
CONFIG_PATH = "ai_navigation/data/config-feedforward.txt"

# Font constants
pygame.font.init()
STAT_FONT = pygame.font.SysFont("dejavusansmono", 50)

# Window positioning
WINDOW_POS_X = 0
WINDOW_POS_Y = 30

# Training simulation defaults
DEFAULT_MAX_FRAMES_ELAPSED = 400
DEFAULT_NO_PROGRESS_FRAMES_ELAPSED = 50

# AI control thresholds
AI_ROTATION_THRESHOLD_HIGH = 0.4
AI_ROTATION_THRESHOLD_LOW = -0.6
AI_ACCELERATION_THRESHOLD = 0.3

# Rotation values
ROTATION_RATE_FAST = 5
ROTATION_RATE_NONE = 0

# Fitness rewards/penalties
FITNESS_REWARD_FORWARD = 0.1
FITNESS_PENALTY_BACKWARD = 0.5

# Vision normalization
VISION_ANGLE_FRONT = -90
VISION_ANGLE_MID_RIGHT = -45
VISION_ANGLE_MID_LEFT = 45
VISION_ANGLE_MID_MID_RIGHT = -67.5
VISION_ANGLE_MID_MID_LEFT = 67.5
VISION_ANGLE_BACK = 90

# Colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_RED_DARK = (200, 50, 50)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_BLUE_DARK = (0, 25, 255)
COLOR_CYAN = (0, 128, 128)
COLOR_MAGENTA = (255, 0, 255)
COLOR_NOT_CROSSED = (190, 190, 0)
COLOR_CROSSED = (255, 255, 0)
COLOR_PURPLE = (140, 124, 215)
COLOR_LIGHT_PINK = (255, 128, 128)

# Vision offset
VISION_OFFSET_DISTANCE = 20

# Fitness line look-back
FITNESS_LOOKBACK_DISTANCE = 4
